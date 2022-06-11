from typing import Optional
from pydantic import BaseModel, constr


class GenreSchema(BaseModel):
    genre: constr(max_length=255)


class GenreOrm(GenreSchema):
    id: Optional[int]

    class Config:
        orm_mode = True
