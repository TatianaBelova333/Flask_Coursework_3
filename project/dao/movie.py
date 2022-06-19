from flask import current_app
from sqlalchemy import desc
from project.dao.base import BaseDAO
from project.dao.models import Movie


class MovieDAO(BaseDAO):

    def get_by_id(self, movie_id):
        return self._db_session.query(Movie).filter(Movie.id == movie_id).one_or_none()

    def get_all(self, filters):
        movies = self._db_session.query(Movie)
        if filters.get('status') == 'new':
            movies = movies.order_by(desc(Movie.year))
        if filters.get('page') is not None:
            page_num = filters.get('page')
            items_per_page = current_app.config["ITEMS_PER_PAGE"]
            offset_value = (page_num - 1) * items_per_page
            movies = movies.limit(items_per_page).offset(offset_value)
            return movies
        return movies.all()
