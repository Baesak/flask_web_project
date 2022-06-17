from . import db


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.VARCHAR(255), unique=True)

    def __str__(self):
        return f"Genre({self.genre})"
