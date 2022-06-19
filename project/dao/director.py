from flask import current_app
from project.dao.base import BaseDAO
from project.dao.models import Director


class DirectorDAO(BaseDAO):

    def get_by_id(self, director_id):
        return self._db_session.query(Director).filter(Director.id == director_id).one_or_none()

    def get_all(self):
        return self._db_session.query(Director).all()

    def filter_by_page(self, page_num):
        items_per_page = current_app.config["ITEMS_PER_PAGE"]
        offset_value = (page_num - 1) * items_per_page
        directors_per_page = self._db_session.query(Director).limit(items_per_page).offset(offset_value)
        return directors_per_page
