import pytest
from app import Flask, Api
from app.utils import login
from app.domain import schemas
from app.data import repos
from app.domain.models.db import db
from app.utils.config import POSTGRES_USER, POSTGRES_PASSWORD
from . import faker


def create_film(title):
    repos.film_repo.create(schemas.NewFilmSchema(title=title, description=faker.text(),
                           poster=faker.image_url(), release_date=faker.date(),
                           rating=faker.pyfloat(right_digits=1, min_value=0.0, max_value=10.0),
                           director_id=1, user_id=1, genres=["Action", "Drama"]))


@pytest.fixture
def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
                                            f"@localhost:5432/test"
    db.init_app(app)

    return app


@pytest.fixture
def db_setup():
    db.create_all()
    repos.genre_repo.create(schemas.GenreSchema(genre="Action"))
    repos.genre_repo.create(schemas.GenreSchema(genre="Drama"))
    repos.director_repo.create(schemas.NewDirectorSchema(first_name="test",
                                                         last_name="test", age=20))
    repos.user_repo.create(schemas.NewUserSchema(username="test", password="test",
                                                 admin_bool=False, email="testtest@gmail.com"))
    repos.user_repo.create(schemas.NewUserSchema(username="test_admin", password="test",
                                                 admin_bool=True, email="testtest@gmail.com"))

    create_film("test1")
    create_film("test2")
    create_film("test3")

    yield None

    db.session.remove()
    db.drop_all()

