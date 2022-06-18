from typing import Optional
from pydantic import BaseModel, constr, EmailStr


class NewUserSchema(BaseModel):
    username: constr(max_length=255)
    password: constr(max_length=255)
    email: EmailStr
    admin_bool: bool


class UserSchema(BaseModel):
    username: Optional[constr(max_length=255)]
    password: Optional[constr(max_length=255)]
    email: Optional[EmailStr]
    admin_bool: bool


class UserLogin(BaseModel):
    username: constr(max_length=255)
    password: constr(max_length=255)


class GetUserSchema(BaseModel):
    username: constr(max_length=255)


class UserOrm(UserSchema):
    id: Optional[int]

    class Config:
        orm_mode = True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
