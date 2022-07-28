import pytest
from unittest.mock import Mock, MagicMock
from app.exceptions.exceptions import MissingData, \
    FilmOperationsError, UserAlreadyExists, NoAccessError, AuthenticationError
from app.domain.service import FilmGet, FilmUtilsMixin, FilmAction,\
    UserGet, UserAction


def test_find_film_bad_input(monkeypatch):
    monkeypatch.setattr("app.domain.schemas.GetDirectorSchema", MagicMock())
    monkeypatch.setattr("app.domain.schemas.GetFilmSchema", MagicMock())
    utils_mixin = FilmUtilsMixin(Mock(get=MagicMock(return_value=None)),
                                 Mock(get=MagicMock(return_value=Mock(id=1))))

    with pytest.raises(MissingData):
        utils_mixin._find_film("test", "test_test")


def test_find_director_bad_input(monkeypatch):
    monkeypatch.setattr("app.domain.schemas.GetDirectorSchema", MagicMock())
    utils_mixin = FilmUtilsMixin(Mock(), Mock(get=MagicMock(return_value=None)))

    with pytest.raises(MissingData):
        utils_mixin._find_director("test_test")


def test_find_films_with_title(monkeypatch):
    film_get = FilmGet(Mock(get_films_by_title=MagicMock(return_value=["test"])),
                       Mock())
    monkeypatch.setattr("app.domain.schemas.GetFilmByTitle", MagicMock())

    result = film_get.find_film_by_title("test", 1, 10)

    assert result[0]["films"] == ["test"]
    assert result[1] == 206


def test_get_film(monkeypatch):
    film_get = FilmGet(Mock(get=MagicMock(return_value=Mock(dict=MagicMock(return_value="test")))),
                       Mock(get=MagicMock(return_value=Mock(id=1))))
    monkeypatch.setattr("app.domain.schemas.GetFilmByTitle",  MagicMock())
    monkeypatch.setattr("app.domain.schemas.GetDirectorSchema", MagicMock())
    monkeypatch.setattr("app.domain.schemas.GetFilmSchema", MagicMock())

    result = film_get.\
        get_film("test", "test_test")

    assert result[0]["film"] == "test"
    assert result[1] == 200


def test_sort_films(monkeypatch):
    film_get = FilmGet(Mock(get_films_with_sort=MagicMock(return_value=["test"])),
                       Mock(get=MagicMock(return_value=Mock(id=1))))
    monkeypatch.setattr("app.domain.schemas.SortFilmSchema", MagicMock())

    result = film_get.sort_films("test", "test", 1, 10)

    assert result[0]["films"] == ["test"]
    assert result[1] == 206


def test_filter_films(monkeypatch):
    film_get = FilmGet(Mock(get_films_with_filter=MagicMock(return_value=["test"])),
                       Mock(get=MagicMock(return_value=Mock(id=1))))
    mock_request = Mock(args=Mock(get=MagicMock(), getlist=MagicMock()))
    monkeypatch.setattr("app.domain.schemas.FilterFilmSchema", MagicMock())
    monkeypatch.setattr("app.domain.schemas.GetDirectorSchema", MagicMock())

    result = film_get.filter_films(mock_request, 1, 10)

    assert result[0]["films"] == ["test"]
    assert result[1] == 206


def test_delete_film(monkeypatch):
    film_repo = Mock(delete=MagicMock(), get=MagicMock(
        return_value=Mock(user_id=1, dict=MagicMock(return_value="test"))))
    film_action = FilmAction(film_repo,  Mock(get=MagicMock(return_value=Mock(id=1))))
    monkeypatch.setattr("app.domain.schemas.GetDirectorSchema", MagicMock())
    monkeypatch.setattr("app.domain.schemas.GetFilmSchema", MagicMock())
    monkeypatch.setattr("flask_login.utils._get_user", MagicMock(return_value=Mock(id=1)))

    result = film_action.delete_film("test", "test_test")

    assert result[0]["deleted_film"] == "test"
    assert result[1] == 200


def test_create_film(monkeypatch):
    film_repo = Mock(create=MagicMock(
        return_value=Mock(title="test", username="test", dict=MagicMock(return_value="test"))))
    film_action = FilmAction(film_repo, Mock(get=MagicMock(return_value=Mock(id=1))))
    monkeypatch.setattr("app.domain.schemas.NewFilmSchema", Mock())
    monkeypatch.setattr("app.domain.schemas.GetDirectorSchema", MagicMock())
    monkeypatch.setattr("flask_login.utils._get_user", MagicMock(return_value=Mock(id=1)))
    mock_request = Mock(args=Mock(get=MagicMock(), getlist=MagicMock()))

    result = film_action.create_film(mock_request)

    assert result[0]["new_film"] == "test"
    assert result[1] == 201


def test_update_film(monkeypatch):
    film_repo = Mock(get_with_id=MagicMock(return_value=Mock(dict=MagicMock(return_value="test"))),
                     update=MagicMock())
    film_action = FilmAction(film_repo,  Mock(get=MagicMock(return_value=Mock(id=1))))
    monkeypatch.setattr("app.domain.schemas.GetDirectorSchema", MagicMock())
    monkeypatch.setattr("app.domain.schemas.GetFilmSchema", MagicMock())
    monkeypatch.setattr("app.domain.schemas.GetFromIdSchema", MagicMock())
    monkeypatch.setattr("app.domain.schemas.FilmSchema", MagicMock())
    monkeypatch.setattr("flask_login.utils._get_user", MagicMock(return_value=Mock(id=1)))
    mock_request = Mock(args=Mock(get=MagicMock(), getlist=MagicMock()))

    result = film_action.update_film("test", "test_test", mock_request)

    assert result[0]["updated_film"] == "test"
    assert result[1] == 200


def test_check_permission_bad_input(monkeypatch):
    film_action = FilmAction(Mock(), Mock())
    monkeypatch.setattr("flask_login.utils._get_user", MagicMock(
        return_value=Mock(id=1, admin_bool=False)))

    with pytest.raises(FilmOperationsError):
        film_action._check_film_permission(Mock(user_id=2))


def test_create_user(monkeypatch):
    user_repo = Mock(get=MagicMock(return_value=None),
                     create=MagicMock(return_value=
                                      Mock(username="test", dict=MagicMock(return_value="test"))))
    user_action = UserAction(user_repo)
    monkeypatch.setattr("app.domain.schemas.NewUserSchema", MagicMock())
    monkeypatch.setattr("app.domain.schemas.GetUserSchema", MagicMock())
    mock_request = Mock(args=Mock(get=MagicMock(), getlist=MagicMock()))

    result = user_action.create_user(mock_request)

    assert result[0]["new_user"] == "test"
    assert result[1] == 201


def test_create_user_bad_input(monkeypatch):
    user_action = UserAction(Mock(get=MagicMock(return_value=True)))
    monkeypatch.setattr("app.domain.schemas.GetUserSchema", Mock())

    with pytest.raises(UserAlreadyExists):
        user_action.create_user(MagicMock())


def test_make_admin(monkeypatch):
    user_repo = Mock(get=MagicMock(return_value=Mock(id=1)),
                     get_with_id=MagicMock(return_value=Mock(dict=MagicMock(return_value="test"))),
                     update=MagicMock())
    user_action = UserAction(user_repo)
    monkeypatch.setattr("app.domain.schemas.GetUserSchema", Mock())
    monkeypatch.setattr("app.domain.schemas.UserSchema", Mock())
    monkeypatch.setattr("flask_login.utils._get_user", MagicMock(return_value=Mock(admin_bool=True)))

    result = user_action.make_admin("test")

    assert result[0]["new_admin"] == "test"
    assert result[1] == 200


def test_make_admin_bad_input(monkeypatch):
    user_action = UserAction(Mock())
    monkeypatch.setattr("flask_login.utils._get_user",
                        MagicMock(return_value=Mock(admin_bool=False)))

    with pytest.raises(NoAccessError):
        user_action.make_admin("test")


def test_login(monkeypatch):
    monkeypatch.setattr("app.domain.schemas.GetUserSchema", Mock())
    user_get = UserGet(Mock(get=MagicMock(return_value=Mock(password="test"))))

    result = user_get.login("test", "test")

    assert isinstance(result, Mock)


def test_login_bad_input(monkeypatch):
    monkeypatch.setattr("app.domain.schemas.GetUserSchema", Mock())
    user_get = UserGet(Mock(get=MagicMock(return_value=Mock(password="test"))))

    with pytest.raises(AuthenticationError):
        user_get.login("test", "password")
