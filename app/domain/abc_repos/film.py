from .base import ModelType, SchemaType, Generic, ABC, abstractmethod, db, Optional


class ABCFilmRepo(ABC, Generic[ModelType, SchemaType]):

    @abstractmethod
    def get_films_by_title(self, session: db.Session) -> Optional[ModelType]:
        ...

    @abstractmethod
    def get_films_with_sort(self, session: db.Session) -> Optional[ModelType]:
        ...

    @abstractmethod
    def get_films_with_filter(self, session: db.Session) -> Optional[ModelType]:
        ...
