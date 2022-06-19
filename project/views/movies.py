from flask import request
from flask_restx import abort, Namespace, Resource, fields

from project.container import movie_service
from project.exceptions import MovieNotFound
from project.views.directors import director_model
from project.views.genres import genre_model

movies_ns = Namespace("movies", description='Movies')

movie_model = movies_ns.model('Movie', {
    "id": fields.Integer(description='Movie id', required=True, example=1),
    "title": fields.String(description='Movie title', required=True, max_length=255, example='Йеллоустоун'),
    "description": fields.String(
        description='Movie description',
        required=True, max_length=255,
        example="Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора "
                "'Ветреной реки'"),
    "trailer": fields.String(description='Movie description', required=True, example="https://www.youtube.com/watch?v"
                                                                                     "=UKei_d0cbP4"),
    "year": fields.Integer(description="Release year", required=True, example=2009),
    "rating": fields.Float(description="Rating", required=True, min=0, max=10, example=8.6),
    "genre": fields.Nested(genre_model),
    "director": fields.Nested(director_model),
    })


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.doc(
        model=movie_model,
        responses={
            200: "OK"
        },
        params={
            "page": {"description": 'page_number', "type": 'int'},
            "status": {"description": "status (can only be new)"}
        }
    )
    def get(self):
        """Get all movies"""
        page_num = request.args.get('page', type=int)
        status = request.args.get('status')
        filters = {
            "page": page_num,
            "status": status,
        }
        return movie_service.get_all_movies(filters)


@movies_ns.route("/<int:movie_id>/")
class MovieView(Resource):
    @movies_ns.doc(
        model=movie_model,
        responses={
            200: "OK",
            404: "Movie not found"
        }
    )
    def get(self, movie_id):
        """Get movie by id"""
        try:
            return movie_service.get_item_by_id(movie_id)
        except MovieNotFound as e:
            print('Movie not found', e)
            abort(404, message=f"Movie_id {movie_id} not found")
