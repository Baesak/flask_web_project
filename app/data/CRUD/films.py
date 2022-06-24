"""Operations for 'Film' model"""

from typing import Generic, Optional
from sqlalchemy.sql.selectable import Subquery
from app.domain.abc_repos.film import ABCFilmRepo
from app.domain import schemas, models
from app.domain.models.db import db
from app.utils.logger import my_logger

from app.utils.custom_types import ModelType, SchemaType
from .base import CRUDBase


class CRUDFilm(CRUDBase, ABCFilmRepo, Generic[ModelType, SchemaType]):

    def __init__(self):
        super().__init__(models.Film, schemas.FilmOrm)

    def create(self, schema: schemas.NewFilmSchema, session: db.Session = db.session) -> Optional[schemas.FilmOrm]:

        schema.genres = self._find_genres(schema.genres)
        return super().create(schema, session)

    def update(self, get_schema: schemas.GetFilmSchema, upd_schema: schemas.FilmSchema,
               session: db.Session = db.session) -> Optional[schemas.FilmOrm]:
        """Convert film genres names list into genre models list before base update."""

        if upd_schema.genres:
            return self._update_with_genres(get_schema, upd_schema, session)

        upd_schema.genres = None
        return self._update(get_schema, upd_schema, session)

    def _update(self, get_schema: schemas.GetFilmSchema, upd_schema: schemas.FilmSchema,
                session: db.Session = db.session):

        return super().update(get_schema, upd_schema, session)

    def _update_with_genres(self, get_schema: schemas.GetFilmSchema, upd_schema: schemas.FilmSchema,
                            session: db.Session = db.session):
        """Makes update with special operations for updating 'genres' list"""

        genres = upd_schema.genres
        upd_schema.genres = None

        update_dict = self._dict_without_none(upd_schema)
        updated_index = self.model.query.filter_by(**get_schema.dict()).update(update_dict)
        self.model.query.get(updated_index).genres = self._find_genres(genres)

        session.commit()
        return self.from_orm_schema.from_orm(updated_index)

    def _find_genres(self, genres_list: list) -> list:
        """Find genre models by genre name."""

        genre_models = [models.Genre.query.filter_by(genre=genre_name).first()
                        for genre_name in genres_list]

        return genre_models

    def get_films_by_title(self, schema: schemas.GetFilmByTitle, page=1, per_page=10) -> Optional[list]:
        """Returning list of films by non-strict title search."""

        models_list = self.model.query.filter(self.model.title.like(f"%{schema.title}%"))\
            .paginate(page=page, per_page=per_page).items
        schemas_list = self._process_models(models_list)

        return schemas_list

    def get_films_with_sort(self, schema: schemas.SortFilmSchema, page=1, per_page=10)\
            -> Optional[list]:
        """Returning sorted films list."""

        models_list = self.model.query.order_by(db.text(f"{schema.sort_by} {schema.sort_type}"))\
            .paginate(page=page, per_page=per_page).items
        schemas_list = self._process_models(models_list)
        return schemas_list

    def get_films_with_filter(self, schema: schemas.FilterFilmSchema, page=1, per_page=10)\
            -> Optional[list]:
        result = db.session.query(self.model).subquery()
        """Returning list of films filtered by some parameters."""

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
        """Filter films by director"""

        return db.session.query(self.model).select_entity_from(subquery).\
            filter(self.model.director_id == director_id).subquery()

    def _filter_by_date(self, subquery: Subquery, date_from: str, date_to: Optional[str]):
        """Filter films by date."""

        if not date_to:
            return db.session.query(self.model).select_entity_from(subquery).\
                filter(self.model.release_date >= date_from).subquery()

        return db.session.query(self.model).select_entity_from(subquery).\
            filter((date_to >= self.model.release_date) &
                   (self.model.release_date >= date_from)).subquery()

    def _filter_by_genres(self, subquery: Subquery, genres: list):
        """Filter films by genres."""

        return db.session.query(self.model).select_entity_from(subquery).\
            filter(self.model.genres.any(models.Genre.genre.in_(genres))).subquery()
