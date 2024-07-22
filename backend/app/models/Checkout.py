from . import db
from .utils import unique_ids
from datetime import datetime

class Checkout(db.Model):
    __tablename__ = 'checkout'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_ids)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_checkout_user'), nullable=False)
    checkout_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    note = db.Column(db.String(500), nullable=True)
    is_returned = db.Column(db.Boolean, default=False)
    return_time = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='checkouts')
