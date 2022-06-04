from pydantic import BaseModel, constr, EmailStr
from typing import Optional


class NewUserSchema(BaseModel):
    username: constr(max_length=255)
    password: constr(max_length=255)
    email: EmailStr
    admin_bool = False


class UserSchema(BaseModel):
    username: Optional[constr(max_length=255)]
    password: Optional[constr(max_length=255)]
    email: Optional[EmailStr]
    admin_bool = False


class UserOrm(UserSchema):
    id: Optional[int]

    class Config:
        orm_mode = True

