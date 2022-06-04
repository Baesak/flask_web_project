from pydantic import BaseModel, constr
from typing import Optional


class GenreSchema(BaseModel):
    genre: constr(max_length=255)


class GenreOrm(GenreSchema):
    id: Optional[int]

    class Config:
        orm_mode = True
