import calendar
import datetime

import jwt
from flask_restx import abort
from project.config import BaseConfig


from project.services import UserService

JWT_SECRET = BaseConfig.SECRET_KEY
JWT_AlGORITHM = BaseConfig.JWT_AlGORITHM
TOKEN_EXPIRE_MINUTES = BaseConfig.TOKEN_EXPIRE_MINUTES
TOKEN_EXPIRE_DAYS = BaseConfig.TOKEN_EXPIRE_DAYS

# Не работает с current_app ???
""""
JWT_SECRET = current_app.config["SECRET_KEY"]
JWT_AlGORITHM = current_app.config["JWT_AlGORITHM"]
TOKEN_EXPIRE_MINUTES = current_app.config["TOKEN_EXPIRE_MINUTES"]
TOKEN_EXPIRE_DAYS = current_app.config["TOKEN_EXPIRE_DAYS"]
"""


class AuthService(UserService):

    def generate_tokens(self, email: str, password: str | None, is_refresh: bool = False):
        user = super().get_by_email(email)

        if user is None:
            abort(401, message='User not found')
        if not is_refresh:
            if not super().compare_passwords(user.password_hash, password):
                abort(401, message='Invalid password')

        payload = {
            "email": user.email,
            "id": user.id
        }

        token_min = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        payload["exp"] = calendar.timegm(token_min.timetuple())
        access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_AlGORITHM)

        token_day = datetime.datetime.utcnow() + datetime.timedelta(days=TOKEN_EXPIRE_DAYS)
        payload["exp"] = calendar.timegm(token_day.timetuple())
        refresh_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_AlGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token: str):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_AlGORITHM])
        email = data.get('email')

        return self.generate_tokens(email=email, password=None, is_refresh=True)