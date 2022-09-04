"""Package with some swagger utils."""

from .request_parsers import create_film_parser, create_user_parser, filter_film_parser
from .user import user
from app import api

api.add_namespace(user, path="/user")
