from pydantic import BaseModel, constr, conint
from typing import Optional


class DirectorSchema(BaseModel):
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    age: Optional[conint(lt=100, gt=0)]


class NewDirectorSchema(BaseModel):
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    age: conint(lt=100, gt=0)


class DirectorOrm(DirectorSchema):

    class Config:
        orm_mode = True
