# user.py
from utility.db_utility import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)
    active = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    date_enabled = db.Column(db.DateTime, nullable=True)

    def is_admin(self):
        return self.role == 'admin'
