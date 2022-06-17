from .db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(255), unique=True)
    password = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(255))
    admin_bool = db.Column(db.BOOLEAN, default=False)

    def __str__(self):
        return f"User({self.username})"

