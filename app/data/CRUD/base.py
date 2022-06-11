from typing import Generic, Type, Optional, TypeVar
from pydantic import BaseModel
from app.domain.abc_repos import ABCBaseRepo
from app.domain.schemas import GetFromIdSchema
from app.domain.models.db import db


ModelType = TypeVar("ModelType", bound=db.Model)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(ABCBaseRepo, Generic[ModelType, SchemaType]):

    def get_with_id(self, schema: GetFromIdSchema) -> Optional[ModelType]:
        return self.model.query.filter_by(id=schema.id).first()

    def get(self, schema: SchemaType):
        return self.model.query.filter_by(**schema.dict()).first()

    def get_all(self) -> Optional[ModelType]:
        return self.model.query.all()

    def create(self, schema: SchemaType, session: db.Session = db.session) -> Optional[ModelType]:
        new = self.model(**schema.dict())

        session.add(new)
        session.commit()

        return new

    def update(self, get_schema: SchemaType, update_schema: SchemaType, session: db.Session = db.session)\
            -> Optional[ModelType]:

        update_dict = {key: value for key, value in update_schema.dict().items() if value is not None}
        updated = self.model.query.filter_by(**get_schema.dict()).update(update_dict)

        session.commit()
        return updated

    def delete(self, schema: SchemaType, session: db.Session = db.session) -> Optional[ModelType]:
        victim = self.get(schema)
        self.model.query.filter_by(**schema.dict()).delete()

        session.commit()
        return victim
