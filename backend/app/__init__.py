from flask import Flask
from app.models import db
from flask_migrate import Migrate
from flask_cors import CORS
from config import ApplicationConfiguration
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from flask_session import Session
jwt = JWTManager()
oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(ApplicationConfiguration)

    # Initialize JWT, Database, CORS, and Migrate with the app
    jwt.init_app(app)
    db.init_app(app)
    oauth.init_app(app)
    CORS(app, supports_credentials=True)
    Migrate(app, db)
    Session(app)
    # Import blueprints 
    from app.auth.endpoints import auth_bp
    from app.contacts.endpoints import contact_bp
    from app.checkouts.endpoints import checkout_bp

    # Register blueprints 
    app.register_blueprint(auth_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(checkout_bp)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
    return app
