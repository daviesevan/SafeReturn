from . import db
from .utils import unique_ids
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_ids)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_notification_user'), nullable=False)
    emergency_contact_id = db.Column(db.Integer, db.ForeignKey('emergency_contact.id', name='fk_notification_contact'), nullable=False)
    notification_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    message = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='sent')  # sent, delivered, etc.

    user = db.relationship('User')
    emergency_contact = db.relationship('EmergencyContact')
