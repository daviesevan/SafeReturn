from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.Relationship import Relationship
from app.models.Contacts import EmergencyContact
from app.models.Users import User
from app.models import db
from sqlalchemy.exc import IntegrityError

contact_bp = Blueprint('contact',
                       __name__,
                       url_prefix='/contact')

@contact_bp.post('/create')
@jwt_required()
def create_contact():
    return jsonify(
        message='create emergency contact endpoint'
    )


@contact_bp.post('/add/relationship')
# @jwt_required()
def add_relationship():
    try:
        data = request.json
        relationship = data.get('relationship')
        if not relationship:
            return jsonify(
                error='Relationship must be provided'
            ), 400
        new_relationship = Relationship(
            relationship=relationship
        )
        db.session.add(new_relationship)
        db.session.commit()
        return jsonify(
            message=f'{relationship} relationship added successfully!'
        ), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            error = 'Relationship already exists in the database'
        )