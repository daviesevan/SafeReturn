from flask import Blueprint, jsonify, request, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.Users import User
from app.models import db
from app.utils import validateEmail, hashPassword, verifyPassword, send_email
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

auth_bp = Blueprint('authentication', __name__, url_prefix='/auth')

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def confirm_reset_token(token :str, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except (SignatureExpired, BadSignature):
        return None
    return email

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
            message=f"Hey there {user.fullname}, welcome back! Usipotee!😁"
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

@auth_bp.post('/forgot-password')
def forgot_password():
    data = request.json
    email = data.get('email')

    if not email or not validateEmail(email):
        return jsonify(error='Please enter a valid email address'), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(error='For some reason, we couldn\'t send you the reset email!'), 404

    token = generate_reset_token(user.email)
    print(token)
    reset_url = f"{request.host_url}auth/reset-password/{token}"

    send_email(user.email, 'Password Reset Request', f'Click here to reset your password: {reset_url}')

    return jsonify(message='Password reset link has been sent to your email'), 200

@auth_bp.post('/reset-password/<token>')
def reset_password(token):
    try:
        email = confirm_reset_token(token)
        if not email:
            return jsonify(error='Invalid or expired token'), 400

        data = request.json
        new_password = data.get('password')
        if not new_password:
            return jsonify(error='Required field was not filled'), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify(error='User not found'), 404

        user.password = hashPassword(new_password)
        db.session.commit()

        return jsonify(message='Password has been reset successfully'), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'Error resetting password: {e}'), 500
    
@auth_bp.put('/update-password')
@jwt_required()
def update_password():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify(error='User not found'), 404

        data = request.json
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify(error='Both current and new passwords are required'), 400

        if not verifyPassword(current_password, user.password):
            return jsonify(error='Current password is incorrect'), 401

        if current_password == new_password:
            return jsonify(error='New password must be different from the current password'), 400

        user.password = hashPassword(new_password)
        db.session.commit()

        return jsonify(message='Password updated successfully'), 200

    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")
        return jsonify(error='An error occurred while updating the password'), 500
