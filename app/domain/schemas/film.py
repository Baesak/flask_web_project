import datetime
from typing import Optional, List, Union
from pydantic import BaseModel, confloat, constr, validator, conint


def check_is_date(value: str) -> str:
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return value
    except ValueError:
        raise ValueError("'release_data' should be data in YYYY-MM-DD format.")


def check_director(value: Union[int, str]):
    if type(value) == str:
        if len(value.split()) != 2:
            raise ValueError("You should enter director's id or full name!")
    return value


class FilmSchema(BaseModel):
    title: Optional[constr(max_length=255)]
    description: Optional[str]
    poster: Optional[str]
    release_date: Optional[constr(max_length=10)]
    director_id: Optional[conint(gt=0)]
    rating: Optional[confloat(lt=10.0, gt=-1)]
    user_id: Optional[conint(gt=0)]
    genres: Optional[List]

    _check_date = validator('release_date', allow_reuse=True)(check_is_date)


class NewFilmSchema(BaseModel):
    title: constr(max_length=255)
    description: Optional[str]
    poster: str
    release_date: constr(max_length=10)
    director: Union[conint(gt=0), constr(max_length=510)]
    genres: List[Union[conint(gt=0), constr(max_length=255)]]
    rating: confloat(lt=10.0, gt=0.0)
    user: Union[conint(gt=0), constr(max_length=255)]

    _check_director = validator('director', allow_reuse=True)(check_director)


class GetFilmSchema(BaseModel):
    title: constr(max_length=255)
    director_id: conint(gt=0)


class GetFilmByTitle(BaseModel):
    title: constr(max_length=255)
    page: conint(gt=0) = 1
    items_per_page: conint(gt=0) = 10


class FilterFilmSchema(BaseModel):
    genres: Optional[List[str]]
    date_from: Optional[constr(max_length=10)]
    date_to: Optional[constr(max_length=10)]
    director: Optional[Union[conint(gt=0), constr(max_length=255)]]
    page: conint(gt=0) = 1
    items_per_page: conint(gt=0) = 10

    _check_date_from = validator("date_from", allow_reuse=True)(check_is_date)
    _check_date_to = validator("date_to", allow_reuse=True)(check_is_date)
    _check_director = validator('director', allow_reuse=True)(check_director)

    @validator("date_to")
    def check_date_params(cls, v, values, **kwargs):
        if not values["date_from"] and v:
            raise ValueError("To filter films by date in some range you should specify date_from and date_to")

        return v


class SortFilmSchema(BaseModel):
    sort_by: str
    page: conint(gt=0) = 1
    items_per_page: conint(gt=0) = 10

    @validator("sort_by")
    def check_sort_option(cls, value):
        if value not in ["release_date", "rating"]:
            raise ValueError("You should choose between 'release_date' and 'rating' sorting"
                             "options")
        return value


class FilmOrm(FilmSchema):
    id: Optional[int]

    class Config:
        orm_mode = True
