import flask_login

from . import db, login_manager  # because it's in __init__, it can be retrieved by "from ."


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
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(64))
    password = db.Column(db.String(64))

    # Favorite quote (o2o)
    fav_quote = db.relationship('Quote', backref="user", uselist=False) # uselist=False <--> OneToOne relationship

    # List of fav books (o2m)
    fav_books = db.relationship("Book", backref="users", secondary=user2book)


