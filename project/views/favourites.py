from flask_restx import Namespace, Resource

from project.container import user_service
from project.schemas import MovieSchema
from project.tools.security import auth_required
from project.views.movies import movie_model

favourites_ns = Namespace("favorites", description="User's favourite movies")
favourites_model = movie_model


@favourites_ns.route("/movies/")
class FavouritesView(Resource):
    @favourites_ns.doc(responses={
        200: "OK",
        401: "Authorization required",
    },  security='apikey',
        model=favourites_model
    )
    @auth_required
    def get(self, user_id):
        """Get user's favourite movies"""
        user = user_service.get_by_id(user_id)
        user_favourites = user.favourite_movies
        return MovieSchema(many=True).dump(user_favourites)


@favourites_ns.route("/movies/<int:movie_id>/")
class FavouriteMovieView(Resource):
    @favourites_ns.doc(responses={
        204: "Deleted",
        401: "Auth required",
        404: "Movie not found",
    }, security='apikey'
    )
    @auth_required
    def post(self, user_id, movie_id):
        """Add movie to favourites"""
        user_service.add_movie_to_favorites(user_id, movie_id)
        return '', 201

    @favourites_ns.doc(responses={
        204: "Deleted",
        401: "Auth required",
        404: "Movie not found",
    }, security='apikey'
    )
    @auth_required
    def delete(self, user_id, movie_id):
        """Delete movie from favourites"""
        user_service.remove_movie_from_favorites(user_id, movie_id)
        return '', 204


