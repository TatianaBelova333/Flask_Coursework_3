from flask import request
from flask_restx import abort, Namespace, Resource, fields
from marshmallow import ValidationError

from project.container import user_service, auth_service
from project.exceptions import BlankRegistrationForm, EmailAlreadyRegistered
from project.schemas import UserSchema


auth_ns = Namespace('auth', description='User registration and authorization')
tokens_model = auth_ns.model('Tokens', {
    "access_token": fields.String(description='Access Token', required=True, example="string"),
    "refresh_token": fields.String(description='Refresh Token', required=True, example="string")
})


@auth_ns.route('/register/')
class RegisterView(Resource):
    @auth_ns.doc(params={
        'email': {"required": True},
        'password': {"required": True}
    },
        responses={
            201: "Created",
            400: "Bad request",
            422: "Email or password fail to meet requirements",
            409: "Record already exists"
        },
    )
    def post(self):
        """Register a new user"""
        entered_data = request.json
        entered_email = entered_data.get('email')
        entered_password = entered_data.get('password')

        try:
            # if email or password form left blank
            if entered_email in ('', None) or entered_password in ('', None):
                raise BlankRegistrationForm

            # if email is already registered
            if user_service.user_exists(entered_email):
                raise EmailAlreadyRegistered

            # validate email address and password
            UserSchema().load({"email": entered_email, "password": entered_password})
            user_service.create(email=entered_email, password=entered_password)
        except ValidationError as e:
            messages = ' '.join(sorted([x[0] for x in e.messages.values()]))
            abort(422, messages)
        except BlankRegistrationForm:
            abort(400, message='Please enter your email and password')
        except EmailAlreadyRegistered:
            abort(409, message='This email is already registered. Please try another one.')

        return "", 201, {"location": "/user/"}


@auth_ns.route('/login/')
class LoginView(Resource):
    @auth_ns.doc(params={
        'email': {"required": True},
        'password': {"required": True}
    },
        responses={
            200: "OK",
            400: "Bad request",
            401: "Invalid credentials",
        },
        model=tokens_model
    )
    def post(self):
        """Authenticate user and generate access and refresh tokens"""
        data = request.json
        entered_email = data.get('email')
        entered_password = data.get('password')
        if entered_email in ('', None) or entered_password in ('', None):
            abort(400, message='Please enter your email and password')
        tokens = auth_service.generate_tokens(email=entered_email, password=entered_password)
        return tokens, 201

    @auth_ns.doc(params={
        'access token': {"required": False},
        'refresh token': {"required": True}
    },
        responses={
            201: "Updated",
            401: "Invalid refresh token",
        },
        model=tokens_model
    )
    def put(self):
        """Update access and refresh tokens"""
        data = request.json
        token = data.get('refresh_token')
        tokens = auth_service.approve_refresh_token(token)
        return tokens, 201