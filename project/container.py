from project.dao import MovieDAO, DirectorDAO, GenreDAO, UserDAO
from project.services import MovieService, DirectorService, GenreService, UserService, AuthService
from project.setup_db import db


movie_dao = MovieDAO(session=db.session)
movie_service = MovieService(dao=movie_dao)

director_dao = DirectorDAO(session=db.session)
director_service = DirectorService(dao=director_dao)

genre_dao = GenreDAO(session=db.session)
genre_service = GenreService(dao=genre_dao)

user_dao = UserDAO(session=db.session)
user_service = UserService(dao=user_dao)

auth_service = AuthService(dao=user_dao)