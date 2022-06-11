from .db import db


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(255))
    last_name = db.Column(db.VARCHAR(255))
    age = db.Column(db.Integer, db.CheckConstraint("100>=age AND age>=18"))

    def __str__(self):
        return f"Director(name:{self.first_name} {self.last_name})"
