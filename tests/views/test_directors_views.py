import pytest

from project.dao.models import Director


@pytest.fixture
def director(db):
    d = Director(name="Квентин Тарантино")
    db.session.add(d)
    db.session.commit()
    return d


class TestDirectorsView:
    url = "/directors/"

    def test_get_directors(self, client, director):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json == [
            {"id": director.id, "name": director.name},
        ]


class TestDirectorView:
    url = "/directors/{director_id}/"

    def test_get_director(self, client, director):
        response = client.get(self.url.format(director_id=director.id))
        assert response.status_code == 200
        assert response.json == {"id": director.id, "name": director.name}

    def test_genre_not_found(self, client):
        response = client.get(self.url.format(director_id=1))
        assert response.status_code == 404

