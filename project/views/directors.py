from flask import request
from flask_restx import abort, Namespace, Resource, fields

from project.container import director_service
from project.exceptions import DirectorNotFound


directors_ns = Namespace("directors", description="Movie directors")

director_model = directors_ns.model('Director', {
    "id": fields.Integer(description='Director id', required=True, example=1),
    'name': fields.String(description='Director name', required=True, max_length=100, example='Квентин Тарантино'),
})


@directors_ns.route("/")
class DirectorsView(Resource):
    @directors_ns.doc(
        model=director_model,
        responses={200: "OK"},
        params={'page': {"description": 'page_number', "type": 'int'}}
    )
    def get(self):
        """Get all directors"""
        page_num = request.args.get('page', type=int)
        if page_num:
            return director_service.get_by_page(page_num)
        return director_service.get_all_directors()


@directors_ns.route("/<int:director_id>/")
class GenreView(Resource):
    @directors_ns.doc(
        model=director_model,
        responses={
            200: "OK",
            404: "Director not found"
        }
    )
    def get(self, director_id: int):
        """Get director by id"""
        try:
            return director_service.get_item_by_id(director_id)
        except DirectorNotFound:
            abort(404, message=f"Director_id {director_id} not found")
