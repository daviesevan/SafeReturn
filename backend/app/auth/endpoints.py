from flask import Blueprint, jsonify, request
# from kinde_sdk import Configuration
import os
import requests
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.Users import User
from app.models import db
from app.utils import validateEmail, hashPassword, verifyPassword

auth_bp = Blueprint('authentication', __name__, url_prefix='/auth')

@auth_bp.post('/signup')
def signup():
    data = request.json
    email = data.get('email')
    fullname = data.get('fullname')
    password = data.get('password')

    if not email or not validateEmail(email):
        return jsonify(error='Invalid email'), 400
    if not fullname or not password:
        return jsonify(error='Full name and password are required'), 400

    if User.query.filter_by(email=email).first():
        return jsonify(error='Email is already registered'), 400

    hashed_password = hashPassword(password)
    new_user = User(email=email, fullname=fullname, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message='User registered successfully'), 201

@auth_bp.post('/login')
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify(error='Email and password are required'), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verifyPassword(password, user.password):
        return jsonify(error='Invalid email or password'), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token
    ), 200
