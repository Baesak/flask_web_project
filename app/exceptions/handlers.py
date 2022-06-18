from app import api
from .exceptions import *
from pydantic.error_wrappers import ValidationError


@api.errorhandler(MissingData)
def handle_missing_data(error: MissingData) -> tuple:
    return {"message": str(error)}, 204


@api.errorhandler(ValidationError)
def handle_wrong_sort_params(error: ValidationError) -> tuple:
    return {"message": str(error)}, 400


@api.errorhandler(UserAlreadyExists)
def handle_user_exists(error: UserAlreadyExists) -> tuple:
    return {"message": "User with that username already exists!"}, 409


@api.errorhandler(AuthenticationError)
def handle_authentication(error: AuthenticationError) -> tuple:
    return {"message": "Invalid username or password"}, 401


@api.errorhandler(NoAccessError)
def handle_no_access(error: NoAccessError):
    return {"message": "Only admin can do that action"}, 401


@api.errorhandler(FilmOperationsError)
def handle_film_operations(error: FilmOperationsError):
    return {"message": "Only user who posted film or admin can do operations with it."}, 401
