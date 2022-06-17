from typing import Optional
from pydantic import BaseModel


class FilmGenre(BaseModel):
    id: Optional[int]
    film_id: Optional[int]
    genre_id: Optional[int]


class FilmGenreOrm(FilmGenre):

    class Config:
        orm_mode = True
