from pydantic import BaseModel
from faker import Faker
from app import app
from app.domain.models.db import db
from app.domain import schemas, models


@app.cli.command('seed')
def seed_db(amount=1000):
    fake = FakeValues()
    session = db.session
    with session.begin():
        for genre in fake.genres_list:
            new_genre = models.Genre(**schemas.GenreSchema(genre=genre).dict())
            session.add(new_genre)

        for _ in range(amount):
            new_director = models.Director(**fake.fake_director().dict())
            session.add(new_director)

            new_user = models.User(**fake.fake_user().dict())
            session.add(new_user)

            new_film = models.Film(**fake.fake_film().dict())
            session.add(new_film)


@app.cli.command('drop_tables')
def drop_tables():
    db.drop_all()
    db.session.commit()


@app.cli.command('create_tables')
def create_tables():
    db.create_all()
    db.session.commit()


class FakeValues:

    genres_list = ["Action", "Comedy", "Drama", "Fantasy", "Horror",
                   "Mystery", "Romance", "Thriller", "Western"]
    user_names = []
    faker = Faker()

    def fake_director(self) -> BaseModel:
        new = schemas.NewDirectorSchema(first_name=self.faker.first_name(),
                                        last_name=self.faker.last_name(),
                                        age=self.faker.random_int(18, 100))
        return new

    def fake_genre(self) -> BaseModel:
        new = schemas.GenreSchema(genre=self.faker.genres())

        return new

    def fake_user(self) -> BaseModel:
        new = schemas.NewUserSchema(username=self._unique_username(), password=self.faker.password(),
                                    email=self.faker.email(), admin_bool=self.faker.pybool())

        return new

    def fake_film(self) -> BaseModel:
        new = schemas.FilmSchema(title=self.faker.sentence(nb_words=4), description=self.faker.text(),
                                 poster=self.faker.image_url(), release_date=self.faker.date(),
                                 rating=self.faker.pyfloat(right_digits=1, min_value=0.0, max_value=10.0),
                                 director_id=self._foreign_key(models.Director),
                                 user_id=self._foreign_key(models.User), genres=self._genres_list_gen())

        return new

    def _foreign_key(self, model) -> int:
        max_id = db.session.query(db.func.max(model.id)).scalar()
        return self.faker.random_int(1, max_id)

    def _unique_username(self) -> str:
        user_name = self.faker.user_name()
        while user_name in self.user_names:
            user_name = self.faker.user_name()

        self.user_names.append(user_name)
        return user_name

    def _genres_list_gen(self) -> list:
        genres_index = {self.faker.random_int(1, len(self.genres_list)) for _ in range(3)}
        genres = [models.Genre.query.filter_by(id=i).first() for i in genres_index]
        return genres
