import pytest

from project.dao import DirectorDAO
from project.dao.models import Director


class TestDirectorDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = DirectorDAO(db.session)

    @pytest.fixture
    def director_1(self, db):
        d = Director(name="Квентин Тарантино")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def director_2(self, db):
        d = Director(name="Евгений Ткачёв")
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_director_by_id(self, director_1):
        assert self.dao.get_by_id(director_1.id) == director_1, "Ошибка поиска director по id"

    def test_get_director_by_id_not_found(self):
        assert self.dao.get_by_id(1) is None, "Ошибка поиска director по несуществующему id"

    def test_get_all_directors(self, director_1, director_2):
        assert self.dao.get_all() == [director_1, director_2], "Ошибка возврата всех directors"