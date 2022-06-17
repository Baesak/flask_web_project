from flask_restx import Resource
from flask_login import login_required, logout_user
from flask import request
from app import api
from .service import user_get, user_action, film_get, film_action


@api.route("/film_title/<string:title>/<int:page>/<int:per_page>")
@api.route("/film_title/<string:title>/<int:page>", defaults={'per_page': 10})
@api.route("/film_title/<string:title>", defaults={'page': 1, 'per_page': 10})
class FilmByTitle(Resource):

    def get(self, title, page=1, per_page=10):
        films_list = film_get.find_film_by_title(title, page, per_page)
        return films_list


@api.route("/film/<string:title>/<string:director>", methods=["GET", "DELETE", "PUT"])
@api.route("/new_film", methods=["POST"])
class Film(Resource):

    def get(self, title, director):
        return film_get.get_film(title, director)

    @login_required
    def delete(self, title, director):
        return film_action.delete_film(title, director)

    @login_required
    def post(self):
        return film_action.create_film(request)

    @login_required
    def put(self, title, director):
        return film_action.update_film(title, director, request)


@api.route("/new_user", methods=["POST"])
@api.route("/make_admin/<string:username>", methods=["PUT"])
class User(Resource):

    def post(self):
        return user_action.create_user(request)

    @login_required
    def put(self, username):
        return user_action.make_admin(username)


@api.route("/login/<string:username>/<string:password>")
class Login(Resource):

    def get(self, username, password):
        return user_get.login(username, password)


@api.route("/logout")
class LogOut(Resource):

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

    def get(self, sort_by, sort_type, page, per_page):
        return film_get.sort_films(sort_by, sort_type, page, per_page)


@api.route("/filter_films", defaults={'page': 1, 'per_page': 10})
@api.route("/filter_films/<int:page>", defaults={'per_page': 10})
@api.route("/filter_films/<int:page>/<int:per_page>")
class FilterFilms(Resource):

    def get(self, page, per_page):
        return film_get.filter_films(request, page, per_page)
