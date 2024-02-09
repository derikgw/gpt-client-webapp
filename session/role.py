# Assuming you have a role.py file with the Role class defined as follows:

# role.py
from utility.db_utility import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # other fields and methods for the Role class


