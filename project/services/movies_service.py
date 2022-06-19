from project.dao import MovieDAO
from project.exceptions import MovieNotFound
from project.schemas import MovieSchema


class MovieService():
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_item_by_id(self, movie_id):
        movie = self.dao.get_by_id(movie_id)
        if not movie:
            raise MovieNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self, filters: dict):
        movies = self.dao.get_all(filters)
        return MovieSchema(many=True).dump(movies)
