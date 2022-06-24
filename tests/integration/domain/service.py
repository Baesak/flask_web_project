from datetime import datetime
from unittest.mock import Mock, MagicMock
import pytest
from app.domain.service import FilmAction, FilmGet, UserAction
from app.data import repos


class Request:

    def __init__(self, params_dict):
        self.params = params_dict

    def get(self, param):
        return self.params[param]

    def getlist(self, param):
        return ["Action", "Drama"]


@pytest.fixture
def create_request():
    return Mock(args=Request({"title": "text", "description": "text",
                              "poster": "https://placeimg.com/505/0/any",
                              "release_date": datetime(2000, 12, 12),
                              "rating": 2.5, "director_name": "test_test",
                              "genres": ["Action", "Drama"]}))


@pytest.fixture
def request_update():
    return Mock(args=Request({"title": "text", "description": "other",
                              "poster": "https://placeimg.com/505/0/other",
                              "release_date": datetime(2000, 10, 12),
                              "rating": 2.5, "director_name": "test_test"}))


class TestFilmAction:

    @pytest.fixture
    def film_action(self):
        return FilmAction(repos.film_repo, repos.director_repo)

    def test_create_film(self, monkeypatch, db_setup,
                         create_request, film_action):
        monkeypatch.setattr("flask_login.utils._get_user", MagicMock(Mock(id=1)))

        result = film_action.create_film(create_request)

        assert isinstance(result[0]["new_film"], dict)
        assert result[1] == 201

    def test_delete_film(self, monkeypatch, db_setup, film_action):
        monkeypatch.setattr("flask_login.utils._get_user", MagicMock(Mock(id=1, admin_bool=False)))

        result = film_action.delete_film("test1", "test_test")

        assert isinstance(result[0]["deleted_film"], dict)
        assert result[1] == 200

    def test_update_film(self, monkeypatch, db_setup, film_action, request_update):
        monkeypatch.setattr("flask_login.utils._get_user", Mock())

        result = film_action.update_film("test1", "test_test", request_update)

        assert isinstance(result[0]["updated_film"], dict)
        assert result[1] == 200


class TestFilmGet:

    @pytest.fixture
    def request_filter(self):
        return Mock(args=Request({"date_from": '2002-12-12', "date_to": '2005-12-12',
                                  "director_name": "test_test"}))

    @pytest.fixture
    def film_get(self):
        return FilmGet(repos.film_repo, repos.director_repo)

    def test_get_film(self, db_setup, film_get):
        result = film_get.get_film("test1", "test_test")

        assert isinstance(result[0]["film"], dict)
        assert result[1] == 200

    def test_find_film_by_title(self, db_setup, film_get):
        result = film_get.find_film_by_title("test", 1, 10)

        assert isinstance(result[0]["films"], list)
        assert result[1] == 206

    def test_sort_films(self, db_setup, film_get):
        result = film_get.sort_films("rating", "asc", 1, 10)

        assert isinstance(result[0]["films"], list)
        assert result[1] == 206

    def test_filter_films(self, db_setup, film_get, request_filter):
        result = film_get.filter_films(request_filter, 1, 10)

        assert isinstance(result[0]["films"], list)
        assert result[1] == 206


class TestUserAction:

    @pytest.fixture
    def user_action(self):
        return UserAction(repos.user_repo)

    @pytest.fixture
    def create_user_request(self):
        return Mock(args=Request({"username": "test2", "password": "test",
                                  "email": "testest@gmail.com"}))

    def test_create_user(self, db_setup, user_action, create_user_request):

        result = user_action.create_user(create_user_request)

        assert isinstance(result[0]["new_user"], dict)
        assert result[1] == 201

    def test_make_admin(self, monkeypatch, db_setup, user_action):
        monkeypatch.setattr("flask_login.utils._get_user", MagicMock(Mock(admin_bool=True)))

        result = user_action.make_admin("test")
        print((result[0]["new_admin"]))
        assert isinstance(result[0]["new_admin"], dict)
        assert result[1] == 200

