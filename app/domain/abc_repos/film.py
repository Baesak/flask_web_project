from .base import ModelType, SchemaType, Generic, ABC, abstractmethod, Optional, ABCBaseRepo
from app.domain import schemas, models


class ABCFilmRepo(ABCBaseRepo, ABC):

    @abstractmethod
    def get_films_by_title(self, schema: schemas.GetFilmByTitle, page: int, per_page: int)\
            -> Optional[models.Film]:
        ...

    @abstractmethod
    def get_films_with_sort(self, schema: schemas.SortFilmSchema, page: int, per_page: int)\
            -> Optional[models.Film]:
        ...

    @abstractmethod
    def get_films_with_filter(self, schema: schemas.FilterFilmSchema, page: int, per_page: int)\
            -> Optional[models.Film]:
        ...
