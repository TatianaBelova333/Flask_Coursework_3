from unittest.mock import MagicMock
import pytest
from project.dao import GenreDAO
from project.dao.models import Genre
from project.exceptions import GenreNotFound
from project.services import GenreService
from project.setup_db import db


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

    genre1 = Genre(id=1, name='Comedy')
    genre2 = Genre(id=2, name="Action")
    genre3 = Genre(id=3, name='Documentary')

    genre_dao.get_by_id = MagicMock(return_value=genre1)
    genre_dao.get_all = MagicMock(return_value=[genre1, genre2, genre3])

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(genre_dao)

    def test_get_one(self):
        director = self.genre_service.get_item_by_id(1)
        assert director is not None
        assert director["id"] == 1
        assert isinstance(director, dict)

    def test_get_all(self):
        genres = self.genre_service.get_all_genres()
        assert len(genres) > 0
        assert isinstance(genres, list)

    def test_get_item_by_id_not_found(self, genre_dao):
        genre_dao.get_by_id = MagicMock(return_value=None)
        with pytest.raises(GenreNotFound):
            self.genre_service.get_item_by_id(2)