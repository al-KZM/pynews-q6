import flask_login
from werkzeug import security

from . import db, login_manager  # because it's in __init__, it can be retrieved by "from ."


user2book = db.Table(
    "user2book", # name of the table
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id"), primary_key=True),
    db.Column("book_id", db.Integer(), db.ForeignKey("book.id"), primary_key=True),
) # PK will be a combination of the two (1-2)


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

    mail = db.Column(db.String(254), nullable=True)

    # Favorite quote (o2o)
    fav_quote = db.relationship('Quote', backref="user", uselist=False) # uselist=False <--> OneToOne relationship

    # List of fav books (o2m)
    fav_books = db.relationship("Book", backref="users", secondary=user2book)


    encrypted_credit_card = db.Column(db.String(254)) # my_user.credit_card --> won't give the credit card

    # Fake attribute (doesn't exist in the database)
    # - Control the set() and get() operations

    ##############################
    #
    # >>> my_user.credit_card
    #   1234 5678 6789 1011
    #
    # >>> my_user.credit_card = "0102 0304 0506 0708"
    #   ERROR: 'my_user.credit_card' is not an attribute
    #
    # >>> my_user.encrypted_credit_card
    #   1101 9876 8765 4321
    #
    ##############################

    @hybrid_property  # from sqlalchemy.ext.hybrid import hybrid_property
    def credit_card(self):
        return self.encrypted_credit_card[::-1]

    @credit_card.setter
    def credit_card(self, new_value):
        self.encrypted_credit_card = new_value[::-1]


    def check_password(self, pwd):
        """
        Check given password against the stored hash
        """
        return security.check_password_hash(self.password, pwd)

    def set_password(self, pwd):
        """
        Storing the hash of the password into the database
        """
        hashed = security.generate_password_hash(pwd)
        self.password = hashed


