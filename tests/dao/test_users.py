import pytest

from project.dao import UserDAO
from project.dao.models import User, Movie


class TestUserDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = UserDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        u = User(
            email="kate@mail.ru",
            password_hash=b'fdjgjfngrutgrjnwg',
            name='Kate',
            surname='Hewitt',
            favourite_genre=1,
        )
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def user_2(self, db):
        u = User(
            email="john@mail.ru",
            password_hash=b'fdjgjfngrutgrjnwfdgssg',
            name='John',
            surname='Johnson',
            favourite_genre=2,
        )
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def movie(self, db):
        m = Movie(
            title='Scream',
            description="Horror movie",
            trailer="www.youtube/ssssggggg",
            year=2010,
            rating=8,
            genre_id=5,
            director_id=6,
        )
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_user_by_id(self, user_1):
        assert self.dao.get_by_id(user_1.id) == user_1, "Ошибка возврата пользователя по id"

    def test_get_movie_by_id_not_found(self):
        assert self.dao.get_by_id(1) is None, "Ошибка возврата пользователя по несуществующему id"

    def test_get_all_users(self, user_1, user_2):
        assert self.dao.get_all() == [user_1, user_2], "Ошибка возврата всех пользователей"

    def test_create_user(self):
        new_user = self.dao.create(
            email='Tanya@gmail.com',
            password_hash=b'fdjgjfngrutgrjnwfdgssg',
        )
        assert isinstance(new_user, User), "Новый объект не является объектом класса User"
        assert new_user.email == 'Tanya@gmail.com', "Неверный email нового объекта пользователя"
        assert new_user.password_hash == b'fdjgjfngrutgrjnwfdgssg', "Неверный hash password нового объекта пользователя"

    def test_update_user(self, user_2):
        user = self.dao.update(user_2)
        assert user == user_2, "Ошибка обновления данных пользователя"

    def test_user_exists(self, user_1):
        assert isinstance(self.dao.user_exists("kate@mail.ru"), bool), "Тип возвращаемых данных - не bool"
        assert self.dao.user_exists("kate@mail.ru") is True, "Ошибка проверки существующего пользователя в базе данных"
        assert self.dao.user_exists("john@mail.ru") is False, "Ошибка проверки несуществующего пользователя в базе данных"

    def test_add_movie_to_favorites(self, user_1, movie):
        self.dao.add_movie_to_favorites(user_1.id, movie.id)
        favorite_movies = user_1.favourite_movies
        assert favorite_movies == [movie], "Ошибка возвращения списка favorite movies"
        assert isinstance(favorite_movies[0], Movie), "Возвращается список не с объектами класса Movie"
        assert isinstance(user_1.favourite_movies, list), "Формат возвращаемых данных favorite movies - не список"

    def test_remove_movie_from_favorites(self, user_1, movie):
        self.dao.add_movie_to_favorites(user_1.id, movie.id)
        self.dao.remove_movie_from_favorites(user_1.id, movie.id)
        assert user_1.favourite_movies == [], "Ошибка удаления фильма из favorites"
        assert isinstance(user_1.favourite_movies, list), "Формат возвращаемых данных favorite movies после удаления- не список"

    def test_remove_movie_from_empty_favorites(self, user_1, movie):
        self.dao.remove_movie_from_favorites(user_1.id, movie.id)
        assert user_1.favourite_movies == [], "Ошибка при попытки удаления из пустого списка favorites"
        assert isinstance(user_1.favourite_movies, list), "Формат возвращаемых данных favorite movies - не список"






