from flask import current_app
from project.dao.base import BaseDAO
from project.dao.models import Genre


class GenreDAO(BaseDAO):

    def get_by_id(self, genre_id):
        return self._db_session.query(Genre).filter(Genre.id == genre_id).one_or_none()

    def get_all(self):
        return self._db_session.query(Genre).all()

    def filter_by_page(self, page_num):
        items_per_page = current_app.config["ITEMS_PER_PAGE"]
        offset_value = (page_num - 1) * items_per_page
        genres_per_page = self._db_session.query(Genre).limit(items_per_page).offset(offset_value)
        return genres_per_page

