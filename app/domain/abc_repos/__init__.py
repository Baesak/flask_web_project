from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic, Optional
from pydantic import BaseModel
from app.domain.models import db


ModelType = TypeVar("ModelType", bound=db.Model)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class ABCBaseRepo(ABC, Generic[ModelType, SchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    @abstractmethod
    def get(self, session: db.Session, schema: SchemaType) -> Optional[ModelType]:
        ...

    @abstractmethod
    def get_all(self, session: db.Session, schema: SchemaType) -> Optional[ModelType]:
        ...

    @abstractmethod
    def create(self, session: db.Session, schema: SchemaType) -> Optional[ModelType]:
        ...

    @abstractmethod
    def update(self, session: db.Session, schema: SchemaType) -> Optional[ModelType]:
        ...

    @abstractmethod
    def delete(self, session: db.Session, schema: SchemaType) -> Optional[ModelType]:
        ...
