from pydantic import BaseModel


class GetFromIdSchema(BaseModel):
    id: int


class GetAll(BaseModel):
    items_per_page = 10
