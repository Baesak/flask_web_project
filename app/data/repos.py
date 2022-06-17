from app.data import CRUD
from app.domain import models

film_repo = CRUD.CRUDFilm()
director_repo = CRUD.CRUDBase(models.Director)
user_repo = CRUD.CRUDBase(models.User)
genre_repo = CRUD.CRUDBase(models.Genre)
