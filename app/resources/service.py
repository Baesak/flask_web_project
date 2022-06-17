from app.domain.service import FilmGet, FilmAction, UserGet, UserAction
from app.data import repos

film_get = FilmGet(repos.film_repo, repos.director_repo)
film_action = FilmAction(repos.film_repo, repos.director_repo)
user_get = UserGet(repos.user_repo)
user_action = UserAction(repos.user_repo)
