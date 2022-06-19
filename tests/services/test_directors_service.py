from unittest.mock import MagicMock
import pytest
from project.dao import DirectorDAO
from project.dao.models import Director
from project.exceptions import DirectorNotFound
from project.services import DirectorService
from project.setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    director1 = Director(id=1, name='John Kennedy')
    director2 = Director(id=2, name="Sean Penn")
    director3 = Director(id=3, name='Michael Kors')

    director_dao.get_by_id = MagicMock(return_value=director1)
    director_dao.get_all = MagicMock(return_value=[director1, director2, director3])

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(director_dao)

    def test_get_one(self):
        director = self.director_service.get_item_by_id(1)
        assert director is not None
        assert director["id"] == 1
        assert isinstance(director, dict)

    def test_get_all(self):
        directors = self.director_service.get_all_directors()
        assert len(directors) > 0
        assert isinstance(directors, list)

    def test_get_item_by_id_not_found(self, director_dao):
        director_dao.get_by_id = MagicMock(return_value=None)
        with pytest.raises(DirectorNotFound):
            self.director_service.get_item_by_id(2)

