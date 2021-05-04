"""
Contains all the database models related to authentication
Classes:
    - User
"""
import flask_login
from werkzeug import security
from sqlalchemy.ext.hybrid import hybrid_property

from . import db, login_manager

# Secondary table for the user<->book relationship
user2book = db.Table(
    "user2book",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id"), primary_key=True),
    db.Column("book_id", db.Integer(), db.ForeignKey("book.id"), primary_key=True),
)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class User(db.Model, flask_login.UserMixin): # db.Model is required if you want to create an SQL model
    """
    A class representing a user.

    ...

    Attributes
    ----------
    id : int
        Automatically incremented unique id
    name : str
        Name of the user
    password : str
        Hash of the user's password
    mail : str
        Mail address of the user
    encrypted_credit_card : str
        Encrypted version of the user's credit card
    credit_card : str
        (Hybrid property) Decrypted version of the user's credit card
    fav_quote : Quote
        User's favourite quote
    fav_books : List of Book objects
        User's favourite books

    Methods
    ----------
    check_password(pwd):
        Return if <pwd> is the right password for this user
    set_password(pwd):
        Hash the password and set it as this user's password
    """

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(64)) # TODO: name it password_hash
    mail = db.Column(db.String(254), nullable=True)
    encrypted_credit_card = db.Column(db.String(254))
    fav_quote = db.relationship('Quote', backref="user", uselist=False)
    fav_books = db.relationship("Book", backref="users", secondary=user2book)


    def save(self):
        """
        Saves a user into the DB
        """
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(f"Failed to save user {self}, ignoring")

    @hybrid_property  # from sqlalchemy.ext.hybrid import hybrid_property
    def credit_card(self):
        """
        Hybrid property 'credit_card', wraps self.encrypted_credit_card
        :return: Decrypted credit card value
        """
        return self.encrypted_credit_card[::-1]

    @credit_card.setter
    def credit_card(self, new_value):
        """
        'credit_card' setter
        :param new_value: New credit card value
        """
        self.encrypted_credit_card = new_value[::-1]

    def check_password(self, pwd):
        """
        Check given password against the stored hash

        :param pwd: value to check against the stored password
        :return: True if <pwd> match the stored one else False
        """
        return security.check_password_hash(self.password, pwd)

    def set_password(self, pwd):
        """
        Storing the hash of the password into the database

        :param pwd: new password of the user
        """
        hashed = security.generate_password_hash(pwd)
        self.password = hashed


