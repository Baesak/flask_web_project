from typing import TypeVar
from pydantic import BaseModel
from app.domain.models.db import db

ModelType = TypeVar("ModelType", bound=db.Model)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
