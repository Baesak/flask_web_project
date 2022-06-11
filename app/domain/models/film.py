from .db import db


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(255))
    description = db.Column(db.TEXT)
    poster = db.Column(db.TEXT)
    release_date = db.Column(db.Date)
    director_id = db.Column(db.Integer, db.ForeignKey("director.id", ondelete="SET NULL"))
    rating = db.Column(db.NUMERIC, db.CheckConstraint("0.0<=rating AND rating<=10.0"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    genres = db.relationship("Genre", secondary='film_genre',
                             backref=db.backref("Film"), cascade="all,delete")
    director = db.relationship("Director", backref=db.backref("Film"))

    def __str__(self):
        return f"Film(title:{self.title}, director_id: {self.director_id})"
