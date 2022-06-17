from . import db


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(255))
    description = db.Column(db.TEXT)
    poster = db.Column(db.TEXT)
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    rating = db.Column(db.NUMERIC, db.CheckConstraint("0.0<rating AND rating<10.0"))
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
