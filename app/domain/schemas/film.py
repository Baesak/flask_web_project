import datetime
from typing import Optional, List, Union, Any
from pydantic import BaseModel, confloat, constr, validator, conint, HttpUrl


def check_is_date(value: Union[str, datetime.date]) -> Union[str, datetime.date]:
    if value:
        try:
            if isinstance(value, str):
                datetime.datetime.strptime(value, '%Y-%m-%d')
                return value
        except ValueError:
            raise ValueError("'release_data' should be data in YYYY-MM-DD format.")

        if not isinstance(value, datetime.date):
            raise ValueError("'release_data' should be string or datetime.date object.")
        return value


def check_genre(value: list):
    genres_list = ["Action", "Comedy", "Drama", "Fantasy", "Horror",
                   "Mystery", "Romance", "Thriller", "Western"]
    genres_set = {genre.capitalize() for genre in value}

    if not genres_set.issubset(genres_list):
        raise ValueError(f"There are no such genres! Available genres:"
                         f"{genres_list}")

    return list(genres_set)


class FilmSchema(BaseModel):
    title: Optional[constr(max_length=255)]
    description: Optional[str]
    poster: Optional[HttpUrl]
    release_date: Optional[Union[datetime.datetime, datetime.date,
                                 constr(max_length=10)]]
    director_id: Optional[Union[conint(gt=0)]]
    rating: Optional[confloat(lt=10.0, gt=-1)]
    user_id: Optional[conint(gt=0)]
    genres: Optional[list]

    _check_date = validator("release_date", allow_reuse=True)(check_is_date)


class NewFilmSchema(BaseModel):
    title: constr(max_length=255)
    description: Optional[str]
    poster: HttpUrl
    release_date: Union[constr(max_length=10), datetime.datetime]
    director_id: conint(gt=0)
    genres: list
    rating: confloat(lt=10.0, gt=0.0)
    user_id: conint(gt=0)

    _check_date = validator("release_date", allow_reuse=True)(check_is_date)
    _check_genre = validator("genres", allow_reuse=True)(check_genre)


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
    director_id: Optional[conint(gt=0)]
    page: conint(gt=0) = 1
    items_per_page: conint(gt=0) = 10

    _check_date_from = validator("date_from", allow_reuse=True)(check_is_date)
    _check_date_to = validator("date_to", allow_reuse=True)(check_is_date)
    _check_genre = validator("genres", allow_reuse=True)(check_genre)

    @validator("date_to")
    def check_date_params(cls, value, values, **kwargs):
        if not values["date_from"] and value:
            raise ValueError("To filter films by date in some range you should specify date_from and date_to")

        return value


class SortFilmSchema(BaseModel):
    sort_by: str
    sort_type = "asc"
    page: conint(gt=0) = 1
    items_per_page: conint(gt=0) = 10

    @validator("sort_by")
    def check_sort_option(cls, value):
        if value not in ["release_date", "rating"]:
            raise ValueError("You should choose between 'release_date' and 'rating' sorting"
                             "options")
        return value

    @validator("sort_type")
    def check_sort_type(cls, value):
        if value not in ["desc", "asc"]:
            raise ValueError("You should choose between 'desc' and 'asc' sorting"
                             "types")
        return value


class FilmOrm(FilmSchema):
    id: Optional[int]

    class Config:
        orm_mode = True

    @validator("genres")
    def unpack_genres(cls, value: list):
        return [model.genre if not isinstance(model, str) else model for model in value]

    @validator("release_date")
    def date_to_str(cls, value: datetime.date):
        return value.strftime("%Y-%m-%d")

    @validator("director_id")
    def convert_none(cls, value):
        if not value:
            return "unknown"
        return value
