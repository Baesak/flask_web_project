from pydantic import BaseModel


class GetFromIdSchema(BaseModel):
    id: int

