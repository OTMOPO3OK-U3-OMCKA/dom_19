from setup_db import db

from dao.director import DirectorDAO
from dao.genre import GenreDAO
from dao.movie import MovieDAO
from dao.user import UserDAO

from service.user import UserService
from service.genre import GenreService
from service.director import DirectorService
from service.movie import MovieService
from service.auth import AuthService

user_dao = UserDAO(db.session)
genre_dao = GenreDAO(db.session)
director_dao = DirectorDAO(db.session)
movie_dao = MovieDAO(db.session)


user_service = UserService(user_dao)
genre_service = GenreService(genre_dao)
director_service = DirectorService(director_dao)
movie_service = MovieService(movie_dao)
auth_service = AuthService(user_service)
