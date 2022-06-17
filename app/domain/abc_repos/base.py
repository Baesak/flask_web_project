from abc import ABC, abstractmethod
from typing import Generic, Optional, Type
from pydantic import BaseModel
from app.utils.custom_types import ModelType, SchemaType


class ABCBaseRepo(ABC, Generic[ModelType, SchemaType]):

    def __init__(self, model: Type[ModelType], from_orm_schema: Type[SchemaType]):
        self.model = model
        self.from_orm_schema = from_orm_schema

    @abstractmethod
    def get_with_id(self, schema: BaseModel) -> Optional[Type[SchemaType]]:
        ...

    @abstractmethod
    def get(self,  schema: BaseModel) -> Optional[Type[SchemaType]]:
        ...

    @abstractmethod
    def get_all(self, page: int, per_page: int) -> Optional[ModelType]:
        ...

    @abstractmethod
    def create(self,  schema: BaseModel) -> Optional[Type[SchemaType]]:
        ...

    @abstractmethod
    def update(self, get_schema: BaseModel, update_schema: BaseModel) -> Optional[Type[SchemaType]]:
        ...

    @abstractmethod
    def delete(self, schema: BaseModel) -> None:
        ...
