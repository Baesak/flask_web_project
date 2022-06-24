import pytest
from app import app
from app.utils.config import Config
from app.resources import route
from app.data.repos import user_repo
from app.utils import login
from app.domain.schemas import GetUserSchema
from app.domain.models.db import db
from datetime import datetime
from app.utils.config import POSTGRES_USER, POSTGRES_PASSWORD


@pytest.fixture
def test_client():
    Config.SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://" \
                                     f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/test"
    db.create_all()
    client = app.test_client()
    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()
    Config.SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2:" \
                                     f"//{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/films"


@pytest.fixture
def login_req(test_client):
    with test_client:
        schema = user_repo.get(GetUserSchema(username="test"))

        @app.login_manager.request_loader
        def load_user_from_request(request):
            return schema

        yield None

        @app.login_manager.request_loader
        def load_user_from_request(request):
            return None


@pytest.fixture
def admin_req():
    schema = user_repo.get(GetUserSchema(username="test_admin"))

    @app.login_manager.request_loader
    def load_user_from_request(request):
        return schema

    yield None

    @app.login_manager.request_loader
    def load_user_from_request(request):
        return None


class TestFilmByTitle:

    def test_get(self, test_client, db_setup):
        result = test_client.get("/film_title/test")

        assert isinstance(result.data, bytes)
        assert result.status_code == 206


class TestLogin:

    def test_get(self, test_client, db_setup):
        result = test_client.get("/login/test/test")

        assert isinstance(result.data, bytes)
        assert result.status_code == 200


class TestLogout:

    def test_get(self, test_client, db_setup, login_req):
        result = test_client.get("/logout")

        assert isinstance(result.data, bytes)
        assert result.status_code == 200


class TestSortFilms:

    def test_get(self, test_client, db_setup):
        result = test_client.get("/sort_films/rating/asc")
        assert isinstance(result.data, bytes)
        assert result.status_code == 206

        result = test_client.get("/sort_films/release_date/desc")
        assert isinstance(result.data, bytes)
        assert result.status_code == 206


class TestFilterFilms:

    def test_get(self, test_client, db_setup):
        data = {"genres": ["Action", "Drama"],
                "date_from": "1999-10-10", "date_to": "2005-10-10",
                "director_id": 1}
        result = test_client.get("/filter_films", query_string=data)
        assert isinstance(result.data, bytes)
        assert result.status_code == 206


class TestUser:

    def test_post(self, test_client, db_setup):
        data = {"username": "test2", "password": "test",
                "email": "testtest@gmail.com"}

        result = test_client.post("/new_user", query_string=data)

        assert isinstance(result.data, bytes)
        assert result.status_code == 201

    def test_put(self, test_client, db_setup, admin_req):
        with test_client:

            test_client.get("/login/test/test_admin")
            result = test_client.put("/make_admin/test")

            assert isinstance(result.data, bytes)
            assert result.status_code == 200


class TestFilm:

    def test_get(self, test_client, db_setup):
        result = test_client.get("/film/test1/test_test")

        assert isinstance(result.data, bytes)
        assert result.status_code == 200

    def test_put(self, test_client, db_setup, login_req):
        data = {"title": "new", "description": "new",
                "poster": "https://placeimg.com/505/0/new",
                "release_date": datetime(2003, 10, 10),
                "rating": 6.0, "director_name": "test_test",
                "genres": ["Action"]}

        result = test_client.put("/film/test1/test_test", query_string=data)

        assert isinstance(result.data, bytes)
        assert result.status_code == 200

    def test_post(self, test_client, db_setup, login_req):
        data = {"title": "text", "description": "text",
                "poster": "https://placeimg.com/505/0/any",
                "release_date": datetime(2000, 12, 12),
                "rating": 2.5, "director_name": "test_test",
                "genres": ["Drama", "Action"]}

        result = test_client.post("new_film", query_string=data)

        assert isinstance(result.data, bytes)
        assert result.status_code == 201

    def test_delete(self, test_client, db_setup, login_req):
        result = test_client.delete("/film/test1/test_test")

        assert isinstance(result.data, bytes)
        assert result.status_code == 200
