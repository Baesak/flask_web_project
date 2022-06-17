import datetime
from pydantic import BaseModel, confloat, constr, validator
from typing import Optional, List


def check_is_date(value: str) -> str:
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return value
    except ValueError:
        raise ValueError("'release_data' should be data in YYYY-MM-DD format.")


class FilmSchema(BaseModel):
    title: Optional[constr(max_length=255)]
    description: Optional[str]
    poster: Optional[str]
    release_date: Optional[constr(max_length=10)]
    director_name: Optional[str]
    genres: Optional[List[str]]
    rating: Optional[confloat(lt=10.0, gt=0.0)]
    username: Optional[constr(max_length=255)]

    _check_date = validator('release_date', allow_reuse=True)(check_is_date)


class NewFilmSchema(BaseModel):
    title: constr(max_length=255)
    description: Optional[str]
    poster: str
    release_date: constr(max_length=10)
    director_name: constr(max_length=255)
    genres: List[str]
    rating: confloat(lt=10.0, gt=0.0)
    username: constr(max_length=255)


class GetFilmSchema(BaseModel):
    title = constr(max_length=255)
    director_name = constr(max_length=255)


class GetFilmByTitle(BaseModel):
    title = constr(max_length=255)
    items_per_page = 10


class FilterFilmSchema(BaseModel):
    genres: Optional[List[str]]
    date_from: Optional[constr(max_length=10)]
    date_to: Optional[constr(max_length=10)]
    director_name: Optional[constr(max_length=255)]
    items_per_page = 10

    _check_date_from = validator('date_from', allow_reuse=True)(check_is_date)
    _check_date_to = validator('date_to', allow_reuse=True)(check_is_date)


class SortFilmSchema(BaseModel):
    sort_by: str
    items_per_page = 10

    @validator("sort_by")
    def check_sort_option(self, value):
        if value not in ["date", "rating"]:
            raise ValueError("You should choose between 'date' and 'rating' sorting"
                             "options")
        return value


class FilmOrm(FilmSchema):
    id: Optional[int]

    class Config:
        orm_mode = True
