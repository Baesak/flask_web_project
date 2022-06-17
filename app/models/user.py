from . import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(255), unique=True)
    password = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(255))
    admin_bool = db.Column(db.BOOLEAN, default=False)


