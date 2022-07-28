"""Request parsers for routes."""

from app import api


def create_film_parser():
    create_film_pars = api.parser()
    create_film_pars.add_argument("title", type=str, )
    create_film_pars.add_argument("description", type=str, )
    create_film_pars.add_argument("poster", type=str, help="Url of image")
    create_film_pars.add_argument("release_date", type=str, )
    create_film_pars.add_argument("director_name", type=str, help="Director's name separated by '_'")
    create_film_pars.add_argument("genres", type=str, help="List of genres")
    create_film_pars.add_argument("rating", type=float)

    return create_film_pars


def create_user_parser():
    create_user_pars = api.parser()
    create_user_pars.add_argument("username", type=str)
    create_user_pars.add_argument("password", type=str)
    create_user_pars.add_argument("email", type=str)

    return create_user_pars


def filter_film_parser():
    filter_film_pars = api.parser()
    filter_film_pars.add_argument("genres", type=list, help="List of genres.")
    filter_film_pars.add_argument("date_from", type=str, help="Can work without 'date_to'")
    filter_film_pars.add_argument("date_to", type=str, help="Can't work without 'date_from'")
    filter_film_pars.add_argument("director_name", type=str, help="Director's name separated by '_'")

    return filter_film_pars
