from project.dao.base import BaseDAO
from project.dao.models import User, Movie


class UserDAO(BaseDAO):

    def get_by_id(self, user_id: int):
        return self._db_session.query(User).filter(User.id == user_id).one_or_none()

    def get_by_email(self, email: str):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def create(self, email: str, password_hash: bytes):
        new_user = User(email=email, password_hash=password_hash)
        self._db_session.add(new_user)
        self._db_session.commit()
        return new_user

    def update(self, user):
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def user_exists(self, email):
        return User.query.filter(User.email == email).first() is not None

    def add_movie_to_favorites(self, user_id: int, movie_id: int) -> None:
        user = self.get_by_id(user_id)
        movie = self._db_session.query(Movie).get(movie_id)
        if movie not in user.favourite_movies:
            user.favourite_movies.append(movie)
            self._db_session.commit()

    def remove_movie_from_favorites(self, user_id: int, movie_id: int) -> None:
        user = self.get_by_id(user_id)
        movie = self._db_session.query(Movie).get(movie_id)
        if movie in user.favourite_movies:
            user.favourite_movies.remove(movie)
            self._db_session.commit()
