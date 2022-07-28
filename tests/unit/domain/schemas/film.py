import datetime
from random import shuffle
from unittest.mock import Mock
import pytest
from pydantic.error_wrappers import ValidationError
from tests import faker
from app.domain.schemas.film import (check_is_date, check_genre, FilterFilmSchema,
                                     SortFilmSchema, FilmOrm)


@pytest.mark.parametrize('some_date', [faker.date() for _ in range(100)])
def test_check_is_date(some_date):
    assert check_is_date(some_date) == some_date

    date_obj = datetime.date(*[int(num) for num in some_date.split("-")])
    assert check_is_date(date_obj) == date_obj


@pytest.mark.parametrize('some_date', ['01/12/1990', '10.23.20000', '01.01.2002'])
def test_check_is_date_bad_input(some_date):

    with pytest.raises(ValueError):
        check_is_date(some_date)


def test_check_genre():
    genres = ["Action", "Comedy", "Drama", "Fantasy", "Horror",
              "Mystery", "Romance", "Thriller", "Western"]
    shuffle(genres)

    checked_genres = check_genre(genres)

    assert set(genres) == set(checked_genres)


def test_check_genre_bad_input():
    genres = ["Action", "Comedy", "Drama", "Fantasy", "Horror",
              "Mystery", "Romance", "Thriller", "Western", "Documentary",
              "Music Video"]
    shuffle(genres)

    with pytest.raises(ValueError):
        check_genre(genres)


def test_filter_film_schema():

    with pytest.raises(ValidationError):
        FilterFilmSchema(date_to="1999-08-12")


@pytest.mark.parametrize('params', [["release_date", "asc"], ["rating", "desc"]])
def test_sort_film_schema(params):
    assert SortFilmSchema.check_sort_option(params[0]) == params[0]
    assert SortFilmSchema.check_sort_type(params[1]) == params[1]

    with pytest.raises(ValueError):
        SortFilmSchema.check_sort_option("string")
    with pytest.raises(ValueError):
        SortFilmSchema.check_sort_type("string")


def test_film_orm_unpack_genres():
    mocks_list = [Mock(genre=faker.word()) for _ in range(10)]

    for index, string in enumerate(FilmOrm.unpack_genres(mocks_list)):
        assert string == mocks_list[index].genre


def test_film_orm_convert_none():

    assert FilmOrm.convert_none(None) == 'unknown'
    assert FilmOrm.convert_none("something") == "something"
