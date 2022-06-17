from typing import Generic, Optional
from sqlalchemy.sql.selectable import Subquery
from app.domain.abc_repos.film import ABCFilmRepo
from app.domain import schemas, models
from app.domain.models.db import db
from app.utils.custom_types import ModelType, SchemaType
from .base import CRUDBase


class CRUDFilm(CRUDBase, ABCFilmRepo, Generic[ModelType, SchemaType]):

    def __init__(self):
        super().__init__(models.Film, schemas.FilmOrm)

    def create(self, schema: schemas.NewFilmSchema, session: db.Session = db.session) -> Optional[schemas.FilmOrm]:
        schema.genres = self._find_genres(schema.genres)
        new_model = self.model(**schema.dict())

        session.add(new_model)
        session.commit()

        return self.from_orm_schema.from_orm(new_model)

    def update(self, get_schema: schemas.GetFilmSchema, upd_schema: schemas.FilmSchema,
               session: db.Session = db.session) -> Optional[schemas.FilmOrm]:
        upd_schema.genres = self._find_genres(upd_schema.genres) if upd_schema.genres else None

        upd_dict = {key: value for key, value in upd_schema.dict().items() if value is not None}
        updated_model = self.model.query.filter_by(**get_schema.dict()).update(upd_dict)

        session.commit()
        return self.from_orm_schema.from_orm(updated_model)

    def _find_genres(self, genres_list: list) -> list:
        genre_models = [models.Genre.query.filter_by(genre=genre_name).first()
                        for genre_name in genres_list]

        return genre_models

    def get_films_by_title(self, schema: schemas.GetFilmByTitle, page=1, per_page=10) -> Optional[list]:
        models_list = self.model.query.filter(self.model.title.like(f"%{schema.title}%"))\
            .paginate(page=page, per_page=per_page).items
        schemas_list = self._process_models(models_list)

        return schemas_list

    def get_films_with_sort(self, schema: schemas.SortFilmSchema, page=1, per_page=10)\
            -> Optional[list]:
        models_list = self.model.query.order_by(db.text(f"{schema.sort_by} {schema.sort_type}"))\
            .paginate(page=page, per_page=per_page).items
        schemas_list = self._process_models(models_list)
        return schemas_list

    def get_films_with_filter(self, schema: schemas.FilterFilmSchema, page=1, per_page=10)\
            -> Optional[list]:
        result = db.session.query(self.model).subquery()

        if schema.director_id:
            result = self._filter_by_director(result, schema.director_id)
        if schema.date_from:
            result = self._filter_by_date(result, schema.date_from, schema.date_to)
        if schema.genres:
            result = self._filter_by_genres(result, schema.genres)

        models_list = db.session.query(self.model).select_entity_from(result).\
            paginate(page=page, per_page=per_page).items
        schemas_list = self._process_models(models_list)

        return schemas_list

    def _filter_by_director(self, subquery: Subquery, director_id: int) -> Optional[models.Film]:

        return db.session.query(self.model).select_entity_from(subquery).\
            filter(self.model.director_id == director_id).subquery()

    def _filter_by_date(self, subquery: Subquery, date_from: str, date_to: Optional[str]):
        if not date_to:
            return db.session.query(self.model).select_entity_from(subquery).\
                filter(self.model.release_date >= date_from).subquery()

        return db.session.query(self.model).select_entity_from(subquery).\
            filter((date_to >= self.model.release_date) &
                   (self.model.release_date >= date_from)).subquery()

    def _filter_by_genres(self, subquery: Subquery, genres: list):
        return db.session.query(self.model).select_entity_from(subquery).\
            filter(self.model.genres.any(models.Genre.genre.in_(genres))).subquery()
