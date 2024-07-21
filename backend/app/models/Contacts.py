from . import db
from .utils import unique_ids
from sqlalchemy.dialects.postgresql import JSON

class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_ids)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_contact_user'), nullable=False)
    email = db.Column(db.String(325), unique=True, nullable=False)
    name = db.Column(db.String(325), unique=False, nullable=False)
    phonenumber = db.Column(JSON, nullable=False)
    relationship = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', back_populates='emergency_contact')


