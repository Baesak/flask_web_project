import datetime
from pydantic import BaseModel, confloat, constr, validator
from typing import Optional, List


class FilmSchema(BaseModel):
    title: Optional[constr(max_length=255)]
    description: Optional[str]
    poster: Optional[str]
    release_date: Optional[constr(max_length=10)]
    director_name: Optional[str]
    genres: Optional[List[str]]
    rating: Optional[confloat(lt=10.0, gt=0.0)]
    username: Optional[constr(max_length=255)]

    @validator('release_date')
    def check_is_date(self, value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            raise ValueError("'release_data' should be data in YYYY-MM-DD format.")


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
    director_name = str


class FilmOrm(FilmSchema):
    id: Optional[int]

    class Config:
        orm_mode = True
