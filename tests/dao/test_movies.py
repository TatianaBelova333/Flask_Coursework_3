import pytest

from project.dao import MovieDAO
from project.dao.models import Movie


class TestMovieDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = MovieDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(
            title='Termintar',
            description="Action movie",
            trailer="www.youtube/ssssggggg",
            year=2009,
            rating=6.9,
            genre_id=4,
            director_id=5,
        )
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
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

    def test_get_movie_by_id(self, movie_1):
        assert self.dao.get_by_id(movie_1.id) == movie_1, "Ошибка поиска movie по id"

    def test_get_movie_by_id_not_found(self):
        assert self.dao.get_by_id(1) is None, "Ошибка поиска movie по несуществующему id"

    def test_get_all_movies(self, movie_1, movie_2):
        assert self.dao.get_all({"status": "new", "page": None}) == [movie_2, movie_1], "Ошибка возврата всех movies " \
                                                                                       "с сортировкой  по году (по " \
                                                                                        "убыванию) "
        assert self.dao.get_all({"status": None, "page": None}) == [movie_1, movie_2], "Ошибка возврата всех movies " \
                                                                                       "без фильтров "
