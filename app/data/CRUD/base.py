"""Basic operations with models."""

from typing import Generic, Optional, Type
from pydantic import BaseModel
from app.domain.abc_repos import ABCBaseRepo
from app.domain.schemas import GetFromIdSchema
from app.domain.models.db import db
from app.utils.custom_types import SchemaType, ModelType, SecondSchemaType


class CRUDBase(ABCBaseRepo, Generic[ModelType, SchemaType, SecondSchemaType]):

    def get_with_id(self, schema: GetFromIdSchema) -> Optional[Type[SchemaType]]:
        """Get with id operation"""

        model = self.model.query.filter_by(id=schema.id).first()
        return self.from_orm_schema.from_orm(model) if model else None

    def get(self, schema: SchemaType) -> Optional[Type[SchemaType]]:
        """Get operation"""

        model = self.model.query.filter_by(**schema.dict()).first()
        return self.from_orm_schema.from_orm(model) if model else None

    def get_all(self, page=1, per_page=10) -> Optional[list]:
        """Get all operation"""

        models_list = self.model.query.paginate(page=page,
                                                per_page=per_page).items
        schemas_list = self._process_models(models_list)

        return schemas_list

    def create(self, schema: SchemaType, session: db.Session = db.session) -> Optional[Type[SchemaType]]:
        new_model = self.model(**schema.dict())
        """Create operation"""

        session.add(new_model)
        session.commit()

        return self.from_orm_schema.from_orm(new_model)

    def update(self, get_schema: SchemaType, update_schema: SecondSchemaType, session: db.Session = db.session)\
            -> Optional[Type[SchemaType]]:
        """Update operation"""

        update_dict = self._dict_without_none(update_schema)
        updated_model = self.model.query.filter_by(**get_schema.dict()).update(update_dict)

        session.commit()
        return self.from_orm_schema.from_orm(updated_model)

    def delete(self, schema: SchemaType, session: db.Session = db.session) -> None:
        """Delete operation"""

        self.model.query.filter_by(**schema.dict()).delete()
        session.commit()

    def _process_models(self, models_list: list) -> list:
        """Turn models into pydantic schemas."""

        return [self.from_orm_schema.from_orm(model).dict() for model in models_list]

    def _dict_without_none(self, schema: BaseModel) -> dict:
        """Remove all keys with 'None' values."""
        return {key: value for key, value in schema.dict().items() if value is not None}
