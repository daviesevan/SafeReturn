from flask import Blueprint, jsonify, request
# from kinde_sdk import Configuration
import os
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.Users import User
from app.models import db
from app.utils import validateEmail, hashPassword, verifyPassword
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

auth_bp = Blueprint('authentication', __name__, url_prefix='/auth')

@auth_bp.post('/signup')
def signup():
    try:
        data = request.json
        email = data.get('email')
        fullname = data.get('fullname')
        password = data.get('password')

        if not email or not validateEmail(email):
            return jsonify(error='Please enter a valid email address'), 400
        if not fullname or not password:
            return jsonify(error='Required fields were not filled!'), 400

        if User.query.filter_by(email=email).first():
            return jsonify(error='For some reason, we couldn\'t register you!'), 400

        hashed_password = hashPassword(password)
        new_user = User(email=email, fullname=fullname, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(message='User registered successfully'), 201
    
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e.orig}") 
        return jsonify(error='We\'re quite sorry about this!'), 500
        
    except UnmappedInstanceError as e:
        db.session.rollback()
        print(f"UnmappedInstanceError: {e}") 
        return jsonify(error='Hmm... the data provided doesn\'t look valid'), 400

    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}") 
        return jsonify(error='An error occurred'), 500


@auth_bp.post('/login')
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify(error='Required fields were not filled'), 400

        user = User.query.filter_by(email=email).first()
        if not user or not verifyPassword(password, user.password):
            return jsonify(error='Hmm... the credential provided seem invalid!'), 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
            message="Hey there, welcome back"
        ), 200

    except Exception:
        db.session.rollback()
        return jsonify(error='We are quite sorry about this!'), 500

@auth_bp.post('/refresh')
@jwt_required(refresh=True)
def refresh_access_token():
    try:
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify(error=f'Error refreshing token: {e}'), 401