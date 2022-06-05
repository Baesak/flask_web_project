from pydantic import BaseModel, confloat, constr
from typing import Optional, List


class FilmSchema(BaseModel):
    title: Optional[constr(max_length=255)]
    description: Optional[str]
    poster: Optional[str]
    director_id: Optional[int]
    genres: Optional[List[int]]
    rating: Optional[confloat(lt=10.0, gt=0.0)]
    username: Optional[constr(max_length=255)]


class NewFilmSchema(BaseModel):
    title: constr(max_length=255)
    description: str
    poster: str
    director_name: constr(max_length=255)
    genres: List[int]
    rating: confloat(lt=10.0, gt=0.0)
    username: constr(max_length=255)


class FilmOrm(FilmSchema):
    id: Optional[int]

    class Config:
        orm_mode = True
