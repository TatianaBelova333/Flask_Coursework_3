from unittest.mock import MagicMock
import pytest
from project.dao import UserDAO
from project.dao.models import User
from project.exceptions import UserNotFound
from project.services import UserService
from project.setup_db import db


@pytest.fixture()
def user_dao():
    user_dao = UserDAO(db.session)

    user1 = User(
            id=1,
            email="john@mail.ru",
            password_hash=b'fdjgjfngrutgrjnwfdgssg',
            name='John',
            surname='Johnson',
            favourite_genre=2,
        )
    user2 = User(
            id=2,
            email="kate@mail.ru",
            password_hash=b'fdjgjfngrutgrjnwg',
            name='Kate',
            surname='Hewitt',
            favourite_genre=1,
        )

    user_dao.get_by_id = MagicMock(return_value=user1)
    user_dao.get_by_email = MagicMock(return_value=user2)

    return user_dao


class TestUserService:
    @pytest.fixture(autouse=True)
    def user_service(self, user_dao):
        self.user_service = UserService(dao=user_dao)

    def test_get_by_id(self):
        user = self.user_service.get_by_id(1)
        assert user is not None, "При поиске user по id возвращается None"
        assert user.id is not None, "При поиске user по id возвращается None"

    def test_get_by_id_not_found(self, user_dao):
        user_dao.get_by_id = MagicMock(return_value=None)
        with pytest.raises(UserNotFound):
            self.user_service.get_by_id(2)

    def test_get_by_email(self):
        user = self.user_service.get_by_email("kate@mail.ru")
        assert user is not None, "При поиске user по email возвращается None"
        assert user.email is not None, "При поиске user по email возвращается None"

    def test_get_by_email_not_found(self, user_dao):
        user_dao.get_by_email = MagicMock(return_value=None)
        assert self.user_service.get_by_email("kate@mail.ru") is None, "При поиске несуществующего email возвращаетя " \
                                                                       "не None "
