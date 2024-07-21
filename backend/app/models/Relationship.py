from . import db
from .utils import unique_ids
class Relationship(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_ids)
    relationship = db.Column(db.String(325), unique=True, nullable=False)