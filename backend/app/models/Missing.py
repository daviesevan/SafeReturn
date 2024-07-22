from . import db
from .utils import unique_ids
from datetime import datetime

class MissingPerson(db.Model):
    __tablename__ = 'missing_person'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_ids)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_missing_user'), nullable=False)
    report_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_known_location = db.Column(db.String(325), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_name = db.Column(db.String(325), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='reported')  # reported, found, etc.

    user = db.relationship('User')
