from pydantic import BaseModel
from typing import Optional


class FilmGenreOrm(BaseModel):
    id: Optional[int]
    film_id: Optional[int]
    genre_id: Optional[int]

    class Config:
        orm_mode = True
