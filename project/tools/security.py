import hashlib

import jwt
from flask import current_app, request
from flask_restx import abort
from project.config import BaseConfig


# Не работает с current_app.config["JWT_AlGORITHM"] ????
AlGORITHM = BaseConfig.JWT_AlGORITHM


def generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401, "Invalid credentials")

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        user_id = None
        try:
            user = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[AlGORITHM])
            user_id = user.get('id')

        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401, "Invalid credentials")

        return func(user_id=user_id, *args, **kwargs)

    return wrapper