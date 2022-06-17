from . import db


film_genre = db.Table("film_genre",
                      db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True),
                      db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)
