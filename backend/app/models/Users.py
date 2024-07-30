from . import db
from .utils import unique_ids
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_ids)
    email = db.Column(db.String(325), unique=True, nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(325), nullable=True)
    isEmailVerified = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    emergency_contacts = db.relationship('EmergencyContact', back_populates='user', cascade='all, delete-orphan')
    checkouts = db.relationship('Checkout', back_populates='user', cascade='all, delete-orphan')
