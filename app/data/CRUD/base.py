from typing import Generic, Optional, Type
from pydantic import BaseModel
from app.domain.abc_repos import ABCBaseRepo
from app.domain.schemas import GetFromIdSchema
from app.domain.models.db import db
from app.utils.custom_types import SchemaType, ModelType


class CRUDBase(ABCBaseRepo, Generic[ModelType, SchemaType]):

    def get_with_id(self, schema: GetFromIdSchema) -> Optional[Type[SchemaType]]:
        model = self.model.query.filter_by(id=schema.id).first()
        return self.from_orm_schema.from_orm(model) if model else None

    def get(self, schema: BaseModel) -> Optional[Type[SchemaType]]:
        model = self.model.query.filter_by(**schema.dict()).first()
        return self.from_orm_schema.from_orm(model) if model else None

    def get_all(self, page=1, per_page=10) -> Optional[list]:
        models_list = self.model.query.paginate(page=page,
                                                per_page=per_page).items
        schemas_list = self._process_models(models_list)

        return schemas_list

    def create(self, schema: BaseModel, session: db.Session = db.session) -> Optional[Type[SchemaType]]:
        new_model = self.model(**schema.dict())

        session.add(new_model)
        session.commit()

        return self.from_orm_schema.from_orm(new_model)

    def update(self, get_schema: BaseModel, update_schema: BaseModel, session: db.Session = db.session)\
            -> Optional[Type[SchemaType]]:

        update_dict = {key: value for key, value in update_schema.dict().items() if value is not None}
        updated_model = self.model.query.filter_by(**get_schema.dict()).update(update_dict)

        session.commit()
        return self.from_orm_schema.from_orm(updated_model)

    def delete(self, schema: BaseModel, session: db.Session = db.session) -> None:
        self.model.query.filter_by(**schema.dict()).delete()
        session.commit()

    def _process_models(self, models_list: list) -> list:
        return [self.from_orm_schema.from_orm(model).dict() for model in models_list]
