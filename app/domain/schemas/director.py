from typing import Optional
from pydantic import BaseModel, constr, conint


class DirectorSchema(BaseModel):
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    age: Optional[conint(lt=101, gt=0)]


class NewDirectorSchema(BaseModel):
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    age: conint(lt=101, gt=0)


class GetDirectorSchema(BaseModel):
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)


class DirectorOrm(DirectorSchema):

    class Config:
        orm_mode = True
