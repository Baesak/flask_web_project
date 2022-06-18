from abc import ABC
from flask import request
from flask_login import login_user, current_user
from app.domain import schemas
from app.domain.abc_repos import ABCBaseRepo, ABCFilmRepo
from app.utils.logger import my_logger
from app.exceptions import (MissingData, NoAccessError,
                            UserAlreadyExists, AuthenticationError, FilmOperationsError)


class FilmUtilsMixin(ABC):

    def __init__(self, film_repo: ABCFilmRepo, director_repo: ABCBaseRepo):
        self.film_repo = film_repo
        self.director_repo = director_repo

    def _find_director(self, name: str):
        name_list = name.split("_")

        director_schema = self.director_repo.get(schemas.GetDirectorSchema(first_name=name_list[0],
                                                                           last_name=name_list[1]))
        if not director_schema:
            raise MissingData("There are no such Director in db!")

        return director_schema

    def _find_film(self, title: str, director_name: str):
        director_id = self._find_director(director_name).id
        schema = schemas.GetFilmSchema(title=title, director_id=director_id)

        film_schema = self.film_repo.get(schema)
        if not film_schema:
            raise MissingData("There are no such Film in db!")

        return film_schema


class FilmGet(FilmUtilsMixin):

    def __init__(self, film_repo: ABCFilmRepo, director_repo: ABCBaseRepo):
        super().__init__(film_repo, director_repo)

    def find_film_by_title(self, title, page, per_page):
        schema = schemas.GetFilmByTitle(title=title)
        schemas_list = self.film_repo.get_films_by_title(schema, page, per_page)

        return {'films': schemas_list}, 206

    def get_film(self, title: str, director_name: str):
        film_schema = self._find_film(title, director_name)

        return {"film:": film_schema.dict()}, 200

    def sort_films(self, sort_by: str, sort_type: str, page: int, per_page: int) -> tuple:
        schema = schemas.SortFilmSchema(sort_by=sort_by, sort_type=sort_type,
                                        page=page, per_page=per_page)

        schemas_list = self.film_repo.get_films_with_sort(schema, page, per_page)

        return {"films": schemas_list}, 206

    def filter_films(self, req: request, page: int, per_page: int) -> tuple:
        director_id = None
        if request.args.get("director_name"):
            director_id = self._find_director(req.args.get("director_name")).id

        schema = schemas.FilterFilmSchema(genres=req.args.getlist("genres"),
                                          date_from=req.args.get("date_from"),
                                          date_to=req.args.get("date_to"),
                                          director_id=director_id)

        schemas_list = self.film_repo.get_films_with_filter(schema, page, per_page)

        return {"films": schemas_list}, 206


class FilmAction(FilmUtilsMixin):

    def __init__(self, film_repo: ABCFilmRepo, director_repo: ABCBaseRepo):
        super().__init__(film_repo, director_repo)

    def delete_film(self, title: str, director_name: str) -> tuple:
        film_schema = self._find_film(title, director_name)
        self._check_film_permission(film_schema)

        delete_schema = schemas.GetFilmSchema(title=title, director_id=film_schema.director_id)

        self.film_repo.delete(delete_schema)
        my_logger.info(f"film '{delete_schema.title}' has been deleted by '{current_user.username}'")

        return {"deleted_film": film_schema.dict()}, 200

    def update_film(self, title, director_name, req: request) -> tuple:
        film_schema = self._find_film(title, director_name)
        self._check_film_permission(film_schema)

        new_director_id = self._find_director(req.args.get("director_name")).id \
            if req.args.get("director_name") else None

        get_schema = schemas.GetFilmSchema(title=title, director_id=film_schema.director_id)
        upd_schema = schemas.FilmSchema(title=req.args.get("title"),
                                        description=req.args.get("description"),
                                        poster=req.args.get("poster"),
                                        release_date=req.args.get("release_date"),
                                        director_id=new_director_id,
                                        genres=req.args.getlist("genres"),
                                        rating=req.args.get("rating"))

        self.film_repo.update(get_schema, upd_schema)
        updated_schema = self.film_repo.get_with_id(schemas.GetFromIdSchema(id=film_schema.id))

        no_none_dict = {key: value for key, value in upd_schema.dict().items() if value is not None}
        my_logger.info(f"user '{current_user}' updated film '{updated_schema.title}': {no_none_dict}")

        return {"updated_film": updated_schema.dict()}, 200

    def create_film(self, req: request) -> tuple:
        director_id = self._find_director(req.args.get("director_name")).id

        schema = schemas.NewFilmSchema(title=req.args.get("title"),
                                       description=req.args.get("description"),
                                       poster=req.args.get("poster"),
                                       release_date=req.args.get("release_date"),
                                       director_id=director_id,
                                       genres=req.args.getlist("genres"),
                                       rating=req.args.get("rating"),
                                       user_id=current_user.id)

        new_film_schema = self.film_repo.create(schema)
        my_logger.info(f"User {current_user.username} added film '{new_film_schema.title}'")

        return {"new_film": new_film_schema.dict()}, 201

    def _check_film_permission(self, film):
        if current_user.id != film.user_id and not current_user.admin_bool:
            raise FilmOperationsError


class UserGet:

    def __init__(self, user_repo: ABCBaseRepo):
        self.user_repo = user_repo

    def login(self, username: str, password: str) -> tuple:
        schema = schemas.GetUserSchema(username=username)

        try:
            user_schema = self.user_repo.get(schema)
            if not user_schema or user_schema.password != password:
                raise AuthenticationError
        except ValueError:
            raise AuthenticationError

        login_user(user_schema)
        return {"message": "Successfully logged in."}, 200


class UserAction:

    def __init__(self, user_repo: ABCBaseRepo):
        self.user_repo = user_repo

    def create_user(self, req: request) -> tuple:
        if self.user_repo.get(schemas.GetUserSchema(username=req.args.get("username"))):
            raise UserAlreadyExists

        schema = schemas.NewUserSchema(username=req.args.get("username"),
                                       password=req.args.get("password"),
                                       email=req.args.get("email"),
                                       admin_bool=False)

        new_user_schema = self.user_repo.create(schema)
        my_logger.info(f"user '{new_user_schema.username}' created")

        return {"new_user": new_user_schema.dict()}, 201

    def make_admin(self, username: str) -> tuple:
        if not current_user.admin_bool:
            raise NoAccessError

        user_id = self._find_user(username).id
        get_schema = schemas.GetUserSchema(username=username)
        upd_schema = schemas.UserSchema(admin_bool=True)

        self.user_repo.update(get_schema, upd_schema)
        updated_schema = self.user_repo.get_with_id(schemas.GetFromIdSchema(id=user_id))
        my_logger.info(f"{current_user.username} made {updated_schema} admin")

        return {"new_admin": updated_schema.dict()}, 200

    def _find_user(self, username: str):
        schema = schemas.GetUserSchema(username=username)

        user_schema = self.user_repo.get(schema)
        if not user_schema:
            raise MissingData("There are no such user in db!")

        return user_schema


# class DomainResourcesService:
#
#     def __init__(self, film_repo: ABCFilmRepo, user_repo: ABCBaseRepo, director_repo: ABCBaseRepo):
#         self.film_repo = film_repo
#         self.user_repo = user_repo
#         self.director_repo = director_repo
#
#     def create_user(self, req: request) -> dict:
#         if self.user_repo.get(schemas.GetUserSchema(username=req.args.get("username"))):
#             raise UserAlreadyExists
#
#         schema = schemas.NewUserSchema(username=req.args.get("username"),
#                                        password=req.args.get("password"),
#                                        email=req.args.get("email"),
#                                        admin_bool=False)
#
#         new_user_schema = self.user_repo.create(schema)
#         my_logger.info(f"user '{new_user_schema.username}' created")
#
#         return {"new_user": new_user_schema.dict()}
#
#     def make_admin(self, username: str) -> dict:
#         if not current_user.admin_bool:
#             raise NoAccessError
#
#         user_id = self._find_user(username).id
#         get_schema = schemas.GetUserSchema(username=username)
#         upd_schema = schemas.UserSchema(admin_bool=True)
#
#         self.user_repo.update(get_schema, upd_schema)
#         updated_schema = self.user_repo.get_with_id(schemas.GetFromIdSchema(id=user_id))
#         my_logger.info(f"{current_user.username} made {updated_schema} admin")
#
#         return {"new_admin": updated_schema.dict()}
#
#     def _find_user(self, username: str):
#         schema = schemas.GetUserSchema(username=username)
#
#         user_schema = self.user_repo.get(schema)
#         if not user_schema:
#             raise MissingData("There are no such user in db!")
#
#         return user_schema
#
#     def _check_film_permission(self, film):
#         if current_user.id != film.user_id and not current_user.admin_bool:
#             raise FilmOperationsError
#
#     def _find_film(self, title: str, director_name: str):
#         director_id = self._find_director(director_name).id
#         schema = schemas.GetFilmSchema(title=title, director_id=director_id)
#
#         film_schema = self.film_repo.get(schema)
#         if not film_schema:
#             raise MissingData("There are no such Film in db!")
#
#         return film_schema
#
#     def _find_director(self, name: str):
#         name_list = name.split("_")
#
#         director_schema = self.director_repo.get(schemas.GetDirectorSchema(first_name=name_list[0],
#                                                                            last_name=name_list[1]))
#         if not director_schema:
#             raise MissingData("There are no such Director in db!")
#
#         return director_schema
