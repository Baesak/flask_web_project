from typing import Union, TypeVar, Generic, Optional
from sqlalchemy.sql.selectable import Subquery
from pydantic import BaseModel
from app.domain.abc_repos.film import ABCFilmRepo
from app.domain import schemas, models
from app.domain.models.db import db
from .base import CRUDBase


director_repo = CRUDBase(models.Director)
ModelType = TypeVar("ModelType", bound=db.Model)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDFilm(CRUDBase, ABCFilmRepo, Generic[ModelType, SchemaType]):

    def __init__(self):
        super().__init__(models.Film)

    def get_films_by_title(self, schema: schemas.GetFilmByTitle) -> Optional[models.Film]:
        return self.model.query.filter(self.model.title.like(f"%{schema.title}%")).all()

    def get_films_with_sort(self, schema: schemas.SortFilmSchema) -> Optional[models.Film]:
        return self.model.query.order_by(getattr(self.model, schema.sort_by)).all()

    def get_films_with_filter(self, schema: schemas.FilterFilmSchema) -> Optional[models.Film]:
        result = db.session.query(self.model).subquery()

        if schema.director:
            result = self._filter_by_director(result, schema.director)
        if schema.date_from:
            result = self._filter_by_date(result, schema.date_from, schema.date_to)
        if schema.genres:
            result = self._filter_by_genres(result, schema.genres)

        return db.session.query(result).all()

    @staticmethod
    def _filter_by_director(subquery: Subquery, director_data: Union[str, int]) -> Optional[models.Film]:

        if isinstance(director_data, int):
            director_id = director_data
        else:
            director_data = director_data.split()
            director_id = director_repo.get(schemas.GetDirectorSchema(first_name=director_data[0],
                                            last_name=director_data[1])).id

        return db.session.query(subquery).filter_by(director_id=director_id).subquery()

    def _filter_by_date(self, subquery: Subquery, date_from: str, date_to: Optional[str]):
        if not date_to:
            return db.session.query(subquery).filter(self.model.release_date >= date_from).subquery()

        return db.session.query(subquery).filter((date_to >= self.model.release_date) &
                                                 (self.model.release_date >= date_from)).subquery()

    def _filter_by_genres(self, result: Subquery, genres: list):
        return db.session.query(result).filter(self.model.genres.any(models.Genre.genre.in_(genres))).subquery()
