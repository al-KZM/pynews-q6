# MODELS.py
from . import db  # Database bridge created in __init__.py

class User(db.Model): # db.Model is required if you want to create an SQL model

    # Every attribute is a class variable

    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(64))
    password = db.Column(db.String(64))


