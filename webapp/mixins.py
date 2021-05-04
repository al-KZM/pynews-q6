from datetime import datetime
from . import db

class ModelMixin:

    id          = db.Column(db.Integer(), primary_key=True)
    created_at  = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), onupdate=datetime.now)

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
