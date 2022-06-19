from flask import request
from flask_restx import Namespace, Resource, abort, fields
from marshmallow import ValidationError

from project.container import user_service
from project.exceptions import UserNotFound
from project.schemas import UserSchema
from project.tools.security import auth_required

user_ns = Namespace('user', description="User's profile update")

user_model = user_ns.model('User', {
    "id": fields.Integer(description='User id', required=True, example=1),
    'email': fields.String(description='User email', required=True, max_length=200, example='john@mail.ru'),
    "name": fields.String(description="User's name", max_length=100, example='John'),
    "surname": fields.String(description="User's surnname", max_length=100, example='Kennedy'),
    "favourite_genre": fields.Integer(description="User's favourtite genre", example=1)
})


@user_ns.route('/')
class UserView(Resource):
    @user_ns.doc(
        security='apikey',
        model=user_model,
        responses={
            200: "OK",
            401: "Authorization needed",
            404: "Bad request"
        }
    )
    @auth_required
    def get(self, user_id):
        """Get user profile"""
        try:
            user = user_service.get_by_id(user_id)
            return UserSchema().dump(user), 200
        except UserNotFound as e:
            print("User not found", e)
            abort(404, message=f"User_id {user_id} not found")

    @user_ns.doc(
        security='apikey',
        model=user_model,
        responses={
            200: "OK",
            401: "Authorization needed",
            404: "User not found"
        },
        params={
            "name": "name",
            "surname": "surname",
            "favourite_genre": {"description": "favourite_genre", "type": "int"}
        }
    )
    @auth_required
    def patch(self, user_id):
        """Update user's profile (name, surname, favourite genre)"""
        data = request.json
        data["id"] = user_id
        user_service.partial_update(data)
        return "", 204


@user_ns.route('/password/')
class PasswordChange(Resource):
    @user_ns.doc(
        security='apikey',
        model=user_model,
        responses={
            200: "OK",
            401: "Authorization needed",
            404: "Bad request",
            422: "New password fails to meet requirements"
        },
        params={
            "old_password": "old_password",
            "new_password": "new_password"
        }
    )
    @auth_required
    def put(self, user_id):
        """Change user's password"""
        user = user_service.get_by_id(user_id)
        data = request.json
        data['id'] = user_id
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if user is None:
            abort(404, 'User not found')
        if not user_service.compare_passwords(user.password_hash, old_password):
            abort(401, "Old password is incorrect")
        try:
            UserSchema().load({"password": new_password}, partial=("email",))
            user_service.partial_update(data)
        except ValidationError:
            abort(
                422,
                'New password must contain AT LEAST 6 characters/one capital letter/one small letter/one digit/one '
                'symbol')
        return '', 204
