from flask import request
from flask_restx import abort, Namespace, Resource, fields


from project.container import genre_service
from project.exceptions import GenreNotFound

genres_ns = Namespace("genres", description="Movie genres")


genre_model = genres_ns.model('Genre', {
    "id": fields.Integer(description='Genre id', required=True, example=1),
    'name': fields.String(description='Genre name', max_length=100, required=True, example='Комедия'),
})


@genres_ns.route("/")
class GenresView(Resource):
    @genres_ns.doc(
        params={'page': {"description": 'page_number', "type": 'int'}},
        responses={200: "OK"},
        model=genre_model
    )
    def get(self):
        """Get all genres"""
        page_num = request.args.get('page', type=int)
        if page_num:
            return genre_service.get_by_page(page_num)
        return genre_service.get_all_genres()


@genres_ns.route("/<int:genre_id>/")
class GenreView(Resource):
    @genres_ns.doc(
        responses={
            200: "OK",
            404: "Genre not found"
        },
        model=genre_model,
    )
    def get(self, genre_id: int):
        """Get genre by id"""
        try:
            return genre_service.get_item_by_id(genre_id)
        except GenreNotFound as e:
            print("Genre not found", e)
            abort(404, message=f"Genre_id {genre_id} not found")


