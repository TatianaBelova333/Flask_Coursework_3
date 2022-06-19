from unittest.mock import MagicMock
import pytest
from project.dao import MovieDAO
from project.dao.models import Movie
from project.services import MovieService
from project.setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    movie1 = Movie(
        id=1,
        title='Scream',
        description='Some horror movie',
        trailer='www.youtube/ssss',
        year=2018,
        rating=9.9,
        genre_id=1,
        director_id=1
    )
    movie2 = Movie(
        id=2,
        title='Scream-2',
        description='Another horror movie',
        trailer='www.youtube/ssssggg',
        year=2019,
        rating=7.9,
        genre_id=2,
        director_id=2
    )

    movie_dao.get_by_id = MagicMock(return_value=movie1)
    movie_dao.get_all = MagicMock(return_value=[movie1, movie2])
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_item_by_id(self):
        movie = self.movie_service.get_item_by_id(1)
        assert movie is not None, "При поиске movie по id возвращается None"
        assert movie["id"] is not None, "При поиске movie по id возвращается None"

    def test_get_all_movies(self):
        movies = self.movie_service.get_all_movies(filters={"page": 1, "status": None})
        assert len(movies) > 0, "Возвращается пустой список при возвращении всех фильмов"
        assert isinstance(movies, list), "Формат возвращаемых данных - не список"
