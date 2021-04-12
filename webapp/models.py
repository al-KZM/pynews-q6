# MODELS.py
import flask_login

from . import db, login_manager  # Database bridge created in __init__.py


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class User(db.Model, flask_login.UserMixin): # db.Model is required if you want to create an SQL model
    """
    user
    +-----------+----------------+--------------------+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+--------------------+
    |  id (PK)  |  name (str64)  |  password (str64)  |  fav_quote (int) --> FK to Quote   | fav_quote_id (BTS) |
    +-----------+----------------+--------------------+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+--------------------+
    |           |                |                    |          <Quote> object            |        1           |
    +-----------+----------------+--------------------+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+--------------------+
    """

    # Every attribute is a class variable

    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(64))
    password = db.Column(db.String(64))


    fav_quote = db.relationship('Quote', backref="user", uselist=False) # uselist=False <--> OneToOne relationship


class Quote(db.Model):
    """
    quote
    +-----------+-------------------+--------------------+--------------------+---------------------------------+
    |  id (PK)  |  sentence(str64)  |    author (str64)  |   date (datetime)  |    user_id(int) --> FK to User  |
    +-----------+-------------------+--------------------+--------------------+---------------------------------+
    |           |                   |                    |                    |               3                 |
    +-----------+-------------------+--------------------+--------------------+---------------------------------+
    """

    id = db.Column(db.Integer(), primary_key=True)

    sentence = db.Column(db.String(256), nullable=False)
    author   = db.Column(db.String(64), nullable=True)
    date     = db.Column(db.DateTime(), nullable=True)

    user_id  = db.Column(db.Integer(), db.ForeignKey("user.id"))
