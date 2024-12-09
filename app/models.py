from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    subscription = db.Column(db.String(50), default='Basic')


class ScientificData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    measurement = db.Column(db.Float, nullable=False)
