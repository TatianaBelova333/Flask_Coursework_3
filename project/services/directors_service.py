from project.dao import DirectorDAO
from project.exceptions import DirectorNotFound
from project.schemas import DirectorSchema


class DirectorService():
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_item_by_id(self, director_id: int):
        director = self.dao.get_by_id(director_id)
        if not director:
            raise DirectorNotFound
        return DirectorSchema().dump(director)

    def get_all_directors(self):
        directors = self.dao.get_all()
        return DirectorSchema(many=True).dump(directors)

    def get_by_page(self, page_num):
        directors = self.dao.filter_by_page(page_num)
        return DirectorSchema(many=True).dump(directors)
