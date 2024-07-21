from flask import Blueprint, jsonify, request, redirect
# from kinde_sdk import Configuration
import os
import requests
from flask_jwt_extended import create_access_token
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

