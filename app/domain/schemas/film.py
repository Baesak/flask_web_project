from pydantic import BaseModel, confloat, constr
from typing import Optional, List


class FilmSchema(BaseModel):
    title: Optional[constr(max_length=255)]
    description: Optional[str]
    poster: Optional[str]
    director_name: Optional[str]
    genres: Optional[List[str]]
    rating: Optional[confloat(lt=10.0, gt=0.0)]
    username: Optional[constr(max_length=255)]


class NewFilmSchema(BaseModel):
    title: constr(max_length=255)
    description: str
    poster: str
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
