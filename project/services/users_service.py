import base64
import hmac

from project.exceptions import UserNotFound
from project.tools.security import generate_password_digest
from project.dao import UserDAO


class UserService():
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_by_id(self, user_id: int):
        user = self.dao.get_by_id(user_id)
        if not user:
            raise UserNotFound
        return user

    def get_by_email(self, email: str):
        user = self.dao.get_by_email(email)
        return user

    def user_exists(self, email):
        return self.dao.user_exists(email)

    def create(self, email: str, password: str):
        password_hash = self.generate_user_password(password)
        return self.dao.create(email=email, password_hash=password_hash)

    def partial_update(self, user_data: dict):
        user = self.get_by_id(user_data.get("id"))
        if "name" in user_data:
            user.name = user_data.get('name')
        if "surname" in user_data:
            user.surname = user_data.get('surname')
        if "favourite_genre" in user_data:
            user.favourite_genre = user_data.get('favourite_genre')
        if "new_password" in user_data:
            user.password_hash = self.generate_user_password(user_data.get('new_password'))
        self.dao.update(user)

    def generate_hash_digest(self, password: str):
        hash_digest = generate_password_digest(password)
        return hash_digest

    def generate_user_password(self, password: str) -> bytes:
        hash_digest = self.generate_hash_digest(password)
        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hash: bytes, other_password: str) -> bool:
        decoded_password_hash = base64.b64decode(password_hash)
        other_password_hash = self.generate_hash_digest(other_password)
        return hmac.compare_digest(decoded_password_hash, other_password_hash)

    def remove_movie_from_favorites(self, user_id: int, movie_id: int) -> None:
        return self.dao.remove_movie_from_favorites(user_id, movie_id)

    def add_movie_to_favorites(self, user_id: int, movie_id: int) -> None:
        return self.dao.add_movie_to_favorites(user_id, movie_id)


