# db_utility.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_tables(app):
    with app.app_context():
        db.create_all()


def drop_tables(app):
    with app.app_context():
        db.drop_all()


def init_app(app):
    db.init_app(app)
