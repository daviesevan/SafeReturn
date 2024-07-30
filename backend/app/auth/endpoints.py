import os
from flask import Blueprint, jsonify, request, current_app, url_for, redirect
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.Users import User
from app.models import db
from app.utils import validateEmail, hashPassword, verifyPassword, send_email
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from app import oauth
from urllib.parse import urlencode

auth_bp = Blueprint('authentication', __name__, url_prefix='/auth')


google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

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
    # Update the reset URL to point to your frontend
    reset_url = f"{current_app.config['FRONTEND_URL']}/reset-password/{token}"

    send_email(user.email, 'Password Reset Request', f'Click here to reset your password: {reset_url}')

    return jsonify(message='Password reset link has been sent to your email'), 200


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        email = confirm_reset_token(token)
        if not email:
            return jsonify(error='Invalid or expired token'), 400
        return jsonify(message='Token is valid, you can now reset your password'), 200

    if request.method == 'POST':
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

# Google auth 
@auth_bp.route('/authorize/google')
def google_authorize():
    redirect_uri = url_for('authentication.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/callback/google')
def google_callback():
    try:
        token = google.authorize_access_token()
        userinfo_endpoint = current_app.config['GOOGLE_USERINFO_ENDPOINT']
        resp = google.get(userinfo_endpoint)
        user_info = resp.json()

        email = user_info['email']
        user = User.query.filter_by(email=email).first()

        if not user:
            user = User(email=email, fullname=user_info.get('name'), isEmailVerified=True)
            db.session.add(user)
            db.session.commit()

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        params = urlencode({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': f"Hey there {user.fullname}, welcome back!"
        })
        frontend_url = f"{os.getenv('FRONTEND_URL')}/auth/callback?{params}"
        return redirect(frontend_url)
    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")
        return jsonify(error='An error occurred during Google authentication'), 500
