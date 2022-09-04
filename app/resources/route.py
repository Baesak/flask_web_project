"""App routes."""

from flask_restx import Resource
from flask_login import login_required, logout_user, login_user
from flask import request
from app import api
from .swagger import create_film_parser, create_user_parser,\
    filter_film_parser, user
from .service import user_get, user_action, film_get, film_action


@api.route("/film_title/<string:title>/<int:page>/<int:per_page>")
@api.route("/film_title/<string:title>/<int:page>", defaults={'per_page': 10})
@api.route("/film_title/<string:title>", defaults={'page': 1, 'per_page': 10})
class FilmByTitle(Resource):

    @api.doc(responses={206: "films"}, params={"title": "Film title"},
             description="Find films by non-strict match.")
    def get(self, title, page=1, per_page=10):
        films_list = film_get.find_film_by_title(title, page, per_page)
        return films_list


@api.route("/film/<string:title>/<string:director>", methods=["GET", "DELETE", "PUT"])
@api.route("/new_film", methods=["POST"])
class Film(Resource):

    @api.doc(responses={200: "Success", 204: "Missing data"},
             params={"title": "Film title", "director":
                     "Director's full name separated with '_'."},
             description="Get film")
    def get(self, title, director):
        return film_get.get_film(title, director)

    @login_required
    @api.doc(responses={200: "Success", 204: "Missing data",
                        403: "NoAccessError"},
             params={"title": "Film title", "director":
                     "Director's full name separated with '_'"},
             description="Delete film. Only admin or user who posted film"
                         "could do that action.")
    def delete(self, title, director):
        return film_action.delete_film(title, director)

    @login_required
    @api.doc(responses={201: "Successfully created", 401: "ValidationError",
                        403: "NoAccessError"},
             params={"title": "Film title", "director":
                     "Director's full name separated with '_'"},
             description="Create film. Login required.")
    @api.expect(create_film_parser())
    def post(self):
        return film_action.create_film(request)

    @api.doc(responses={201: "Successfully created", 401: "ValidationError",
                        204: "Missing data", 403: "NoAccessError"},
             params={"title": "Film title", "director":
                     "Director's full name separated with '_'"},
             description="Update film. Only admin or user who posted film"
                         "could do that action.")
    @api.expect(create_film_parser())
    @login_required
    def put(self, title, director):
        return film_action.update_film(title, director, request)


@user.route("/new_user", methods=["POST"])
@user.route("/make_admin/<string:username>", methods=["PUT"])
class User(Resource):

    @user.doc(responses={201: "Successfully created", 401: "ValidationError",
                        409: "UserAlreadyExists"},
             description="Create user.")
    @user.expect(create_user_parser())
    def post(self):
        return user_action.create_user(request)

    @user.doc(responses={201: "Successfully created", 204: "Missing data",
                        403: "NoAccessError"},
             description="Make existing user an admin. Only admin"
                         "could do that action.")
    @login_required
    def put(self, username):
        return user_action.make_admin(username)


@user.route("/login/<string:username>/<string:password>")
class Login(Resource):

    @user.doc(responses={401: "AuthenticationError", 200: "Success"},
              description="Login into account.")
    def get(self, username, password):
        user_schema = user_get.login(username, password)
        login_user(user_schema)
        return {"message": "Successfully logged in."}, 200


@user.route("/logout")
class LogOut(Resource):

    @user.doc(responses={401: "UNAUTHORIZED", 200: "Success"},
             description="Logout. Login required.")
    @login_required
    def get(self):
        logout_user()
        return {"message": "Successfully logged out."}


@api.route("/sort_films/<string:sort_by>",
           defaults={"sort_type": "asc", 'page': 1, 'per_page': 10})
@api.route("/sort_films/<string:sort_by>/<string:sort_type>",
           defaults={'page': 1, 'per_page': 10})
@api.route("/sort_films/<string:sort_by>/<string:sort_type>/<int:page>",
           defaults={'per_page': 10})
@api.route("/sort_films/<string:sort_by>/<string:sort_type>/<int:page>/<int:per_page>")
class SortFilms(Resource):

    @api.doc(responses={401: "ValidationError", 206: "films"},
             description="Sort films by specified parameters. Avaliable parameters -"
                         "sort_by(rating, release_date); sort_type(asc, desc)")
    def get(self, sort_by, sort_type, page, per_page):
        return film_get.sort_films(sort_by, sort_type, page, per_page)


@api.route("/filter_films", defaults={'page': 1, 'per_page': 10})
@api.route("/filter_films/<int:page>", defaults={'per_page': 10})
@api.route("/filter_films/<int:page>/<int:per_page>")
class FilterFilms(Resource):

    @api.doc(responses={401: "ValidationError", 206: "films"},
             description="Filter films by parameters.")
    @api.expect(filter_film_parser())
    def get(self, page, per_page):
        return film_get.filter_films(request, page, per_page)
