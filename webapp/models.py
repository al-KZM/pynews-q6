# MODELS.py
import flask_login

from . import db, login_manager  # Database bridge created in __init__.py


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class User(db.Model, flask_login.UserMixin): # db.Model is required if you want to create an SQL model
    """
    user
    +-----------+----------------+--------------------+
    |  id (PK)  |  name (str64)  |  password (str64)  |
    +-----------+----------------+--------------------+
    |           |                |                    |
    +-----------+----------------+--------------------+
    """

    # Every attribute is a class variable

    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(64))
    password = db.Column(db.String(64))


