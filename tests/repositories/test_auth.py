from unittest import mock
from datetime import datetime

from app.repositories.auth import AuthRepository

TEST_EMAIL = "test@test.com"


@mock.patch("app.db")
@mock.patch("app.repositories.auth.User")
def test_create_user(MockedUser, mocked_db):
    auth_repository = AuthRepository(mocked_db)

    data = {
        "username": "test",
        "email": TEST_EMAIL,
        "password": "test",
    }
    auth_repository.create(data)

    mocked_db.session.add.assert_called_once()
    mocked_db.session.commit.assert_called_once()
    MockedUser.from_dict.assert_called_once_with(data)


@mock.patch("app.db")
@mock.patch("app.repositories.auth.User")
def test_update_user(MockedUser, mocked_db):
    auth_repository = AuthRepository(mocked_db)
    data = {
        "username": "test",
        "email": TEST_EMAIL,
        "fullname": "test",
        "bio": "test",
        "last_login": datetime.utcnow(),
    }
    auth_repository.update(1, data)

    mocked_db.session.commit.assert_called_once()
    MockedUser.query.get.assert_called_once_with(1)


@mock.patch("app.db")
@mock.patch("app.repositories.auth.User")
def test_update_user_not_found(MockedUser, mocked_db):
    MockedUser.query.get.return_value = None

    auth_repository = AuthRepository(mocked_db)
    data = {
        "username": "test",
        "email": TEST_EMAIL,
        "fullname": "test",
        "bio": "test",
        "last_login": datetime.utcnow(),
    }
    auth_repository.update(1, data)

    MockedUser.query.get.assert_called_once_with(1)
    assert MockedUser.query.get(1) is None


@mock.patch("app.db")
@mock.patch("app.repositories.auth.User")
def test_get_user_by_email(MockedUser, mocked_db):
    auth_repository = AuthRepository(mocked_db)
    auth_repository.get_by_email(TEST_EMAIL)

    MockedUser.query.filter_by.assert_called_once_with(email=TEST_EMAIL)


@mock.patch("app.db")
@mock.patch("app.repositories.auth.User")
def test_get_all_users(MockedUser, mocked_db):
    auth_repository = AuthRepository(mocked_db)
    auth_repository.get_all()

    MockedUser.query.limit.assert_called_once()
