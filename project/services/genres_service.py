from project.dao import GenreDAO
from project.exceptions import GenreNotFound
from project.schemas.genre import GenreSchema


class GenreService():
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_item_by_id(self, genre_id: int):
        genre = self.dao.get_by_id(genre_id)
        if not genre:
            raise GenreNotFound
        return GenreSchema().dump(genre)

    def get_all_genres(self):
        genres = self.dao.get_all()
        return GenreSchema(many=True).dump(genres)

    def get_by_page(self, page_num):
        genres = self.dao.filter_by_page(page_num)
        return GenreSchema(many=True).dump(genres)