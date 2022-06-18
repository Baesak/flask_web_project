from app.data import CRUD
from app.domain import models, schemas

film_repo = CRUD.CRUDFilm()
director_repo = CRUD.CRUDBase(models.Director, schemas.DirectorOrm)
user_repo = CRUD.CRUDBase(models.User, schemas.UserOrm)
genre_repo = CRUD.CRUDBase(models.Genre, schemas.GenreOrm)
