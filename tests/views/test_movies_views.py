import pytest

from project.dao.models import Movie


@pytest.fixture
def movie(db):
    m = Movie(
            title='Scream',
            description="Horror movie",
            trailer="www.youtube/ssssggggg",
            year=2010,
            rating=8,
            genre_id=5,
            director_id=7,
        )
    db.session.add(m)
    db.session.commit()
    return m


class TestMoviesView:
    url = "/movies/"

    def test_get_movies(self, client, movie):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json == [
            {
                "id": 1,
                "title": movie.title,
                "description": movie.description,
                "trailer": movie.trailer,
                "year": movie.year,
                "rating": movie.rating,
                "genre": None,
                "director": None
            }
        ]


class TestMovieView:
    url = "/movies/{movie_id}/"

    def test_get_movie(self, client, movie):
        response = client.get(self.url.format(movie_id=movie.id))
        assert response.status_code == 200
        assert response.json == {
                "id": 1,
                "title": movie.title,
                "description": movie.description,
                "trailer": movie.trailer,
                "year": movie.year,
                "rating": movie.rating,
                "genre": None,
                "director": None
            }

    def test_genre_not_found(self, client):
        response = client.get(self.url.format(movie_id=1))
        assert response.status_code == 404
