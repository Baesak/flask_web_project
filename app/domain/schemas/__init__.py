"""Package with pydantic schemas."""

from pydantic import BaseModel, conint
from .film import GetFilmByTitle, GetFilmSchema, FilmSchema, FilterFilmSchema, FilmOrm, SortFilmSchema, NewFilmSchema
from .user import UserSchema, UserOrm, UserLogin, NewUserSchema, GetUserSchema
from .genre import GenreSchema, GenreOrm
from .director import DirectorOrm, DirectorSchema, GetDirectorSchema, NewDirectorSchema
from .film_genre import FilmGenre, FilmGenreOrm


class GetFromIdSchema(BaseModel):
    id: conint(gt=0)


class GetAll(BaseModel):
    page: conint(gt=0) = 1
    items_per_page: conint(gt=0) = 10


class SomeList(BaseModel):
    lst: list
