from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.Relationship import Relationship
from app.models.Contacts import EmergencyContact
from app.models.Users import User
from app.models import db
from sqlalchemy.exc import IntegrityError
from app.auth.utils import validateEmail



contact_bp = Blueprint('contact', __name__, url_prefix='/contact')

@contact_bp.post('/create')
@jwt_required()
def create_contact():
    try:
        data = request.json
        user_id = get_jwt_identity()
        email = data.get('email')
        name = data.get('name')
        phonenumber = data.get('phonenumber')
        relationship = data.get('relationship')

        if not email or not name or not phonenumber or not relationship:
            return jsonify(error='All fields are required'), 400

        if not validateEmail(email):
            return jsonify(error='Invalid email address'), 400

        new_contact = EmergencyContact(
            user_id=user_id,
            email=email,
            name=name,
            phonenumber=phonenumber,
            relationship=relationship
        )

        db.session.add(new_contact)
        db.session.commit()

        return jsonify(message='Emergency contact created successfully'), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify(error='Contact with this email already exists'), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred: {e}'), 500

@contact_bp.get('/users/<int:user_id>/contacts')
@jwt_required()
def get_contacts(user_id):
    try:
        contacts = EmergencyContact.query.filter_by(user_id=user_id).all()
        if not contacts:
            return jsonify(error='No contacts found'), 404

        contacts_list = [{
            'id': contact.id,
            'email': contact.email,
            'name': contact.name,
            'phonenumber': contact.phonenumber,
            'relationship': contact.relationship
        } for contact in contacts]

        return jsonify(contacts=contacts_list), 200

    except Exception as e:
        return jsonify(error=f'An error occurred: {e}'), 500

@contact_bp.put('/update')
@jwt_required()
def update_contact():
    try:
        data = request.json
        user_id = get_jwt_identity()
        contact_id = data.get('contact_id')
        email = data.get('email')
        name = data.get('name')
        phonenumber = data.get('phonenumber')
        relationship = data.get('relationship')

        contact = EmergencyContact.query.filter_by(id=contact_id, user_id=user_id).first()

        if not contact:
            return jsonify(error='Contact not found'), 404

        if email:
            if not validateEmail(email):
                return jsonify(error='Invalid email address'), 400
            contact.email = email
        if name:
            contact.name = name
        if phonenumber:
            contact.phonenumber = phonenumber
        if relationship:
            contact.relationship = relationship

        db.session.commit()

        return jsonify(message='Contact updated successfully'), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred: {e}'), 500

@contact_bp.delete('/delete/<int:contact_id>')
@jwt_required()
def delete_contact(contact_id):
    try:
        user_id = get_jwt_identity()
        contact = EmergencyContact.query.filter_by(id=contact_id, user_id=user_id).first()

        if not contact:
            return jsonify(error='Contact not found'), 404

        db.session.delete(contact)
        db.session.commit()

        return jsonify(message='Contact deleted successfully'), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred: {e}'), 500

@contact_bp.post('/add/relationship')
# @jwt_required()
def add_relationship():
    try:
        data = request.json
        relationship = data.get('relationship')
        if not relationship:
            return jsonify(error='Relationship must be provided'), 400
        new_relationship = Relationship(relationship=relationship)
        db.session.add(new_relationship)
        db.session.commit()
        return jsonify(message=f'{relationship} relationship added successfully!'), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify(error='Relationship already exists in the database'), 400
