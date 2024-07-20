from flask import Blueprint, jsonify

auth_bp = Blueprint('authentication', __name__, url_prefix='/auth')

@auth_bp.post('/signup')
def signup():
    return jsonify(
        message = "this is the signup endpoint"
    )


@auth_bp.post('/login')
def login():
    return jsonify(
        message = "this is the login endpoint"
    )