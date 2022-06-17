from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic, Optional
from pydantic import BaseModel
from app.domain.models.db import db


ModelType = TypeVar("ModelType", bound=db.Model)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class ABCBaseRepo(ABC, Generic[ModelType, SchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    @abstractmethod
    def get_with_id(self, schema: SchemaType) -> Optional[ModelType]:
        ...

    @abstractmethod
    def get(self,  schema: SchemaType) -> Optional[ModelType]:
        ...

    @abstractmethod
    def get_all(self) -> Optional[ModelType]:
        ...

    @abstractmethod
    def create(self,  schema: SchemaType) -> Optional[ModelType]:
        ...

    @abstractmethod
    def update(self, get_schema: SchemaType, update_schema: SchemaType) -> Optional[ModelType]:
        ...

    @abstractmethod
    def delete(self, schema: SchemaType) -> Optional[ModelType]:
        ...
