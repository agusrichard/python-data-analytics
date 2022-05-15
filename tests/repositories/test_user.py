import pytest
from unittest import mock
from datetime import datetime

from app.repositories.user import UserRepository

TEST_EMAIL = "test@test.com"


@pytest.fixture
def auth_repository_db_user():
    with mock.patch("app.repositories.user.SQLAlchemy") as mocked_db:
        with mock.patch("app.repositories.user.User") as MockedUser:
            yield UserRepository(mocked_db), mocked_db, MockedUser


def test_positive_create_user(auth_repository_db_user):
    auth_repository, mocked_db, MockedUser = auth_repository_db_user

    data = {
        "username": "test",
        "email": TEST_EMAIL,
        "password": "test",
    }
    auth_repository.create(data)

    mocked_db.session.add.assert_called_once()
    mocked_db.session.commit.assert_called_once()
    MockedUser.from_dict.assert_called_once_with(data)


def test_positive_get_user_by_id(auth_repository_db_user):
    auth_repository, _, MockedUser = auth_repository_db_user

    auth_repository.get_by_id(1)

    MockedUser.query.get.assert_called_once_with(1)


def test_negative_get_user_by_id_not_found(auth_repository_db_user):
    auth_repository, _, MockedUser = auth_repository_db_user
    MockedUser.query.get.return_value = None

    assert auth_repository.get_by_id(1) is None
    MockedUser.query.get.assert_called_once_with(1)


def test_positive_get_user_by_email(auth_repository_db_user):
    auth_repository, _, MockedUser = auth_repository_db_user

    auth_repository.get_by_email(TEST_EMAIL)

    MockedUser.query.filter_by.assert_called_once_with(email=TEST_EMAIL)


def test_negative_get_user_by_email_not_found(auth_repository_db_user):
    auth_repository, _, MockedUser = auth_repository_db_user
    MockedUser.query.filter_by.return_value.first.return_value = None

    assert auth_repository.get_by_email(TEST_EMAIL) is None
    MockedUser.query.filter_by.assert_called_once_with(email=TEST_EMAIL)
    MockedUser.query.filter_by.return_value.first.assert_called_once()


def test_positive_update_user(auth_repository_db_user):
    auth_repository, mocked_db, MockedUser = auth_repository_db_user

    data = {
        "username": "test",
        "email": TEST_EMAIL,
        "fullname": "test",
        "bio": "test",
        "last_login": datetime.utcnow(),
        "avatar": "test",
    }
    auth_repository.update(1, data)

    mocked_db.session.commit.assert_called_once()
    MockedUser.query.get.assert_called_once_with(1)


def test_negative_update_user_not_found(auth_repository_db_user):
    auth_repository, mocked_db, MockedUser = auth_repository_db_user
    MockedUser.query.get.return_value = None

    data = {
        "username": "test",
        "email": TEST_EMAIL,
        "fullname": "test",
        "bio": "test",
        "last_login": datetime.utcnow(),
        "avatar": "test",
    }
    auth_repository.update(1, data)

    mocked_db.session.commit.assert_not_called()
    MockedUser.query.get.assert_called_once_with(1)


def test_positive_get_all_users(auth_repository_db_user):
    auth_repository, _, MockedUser = auth_repository_db_user

    auth_repository.get_all()

    MockedUser.query.limit.assert_called_once()
    MockedUser.query.limit.return_value.offset.assert_called_once()
    MockedUser.query.limit.return_value.offset.return_value.all.assert_called_once()


def test_positive_get_all_users_with_take_skip(auth_repository_db_user):
    auth_repository, _, MockedUser = auth_repository_db_user

    auth_repository.get_all(take=10, skip=10)

    MockedUser.query.limit.assert_called_once_with(10)
    MockedUser.query.limit.return_value.offset.assert_called_once_with(10)
    MockedUser.query.limit.return_value.offset.return_value.all.assert_called_once()


def test_positive_follow_user(auth_repository_db_user):
    auth_repository, mocked_db, MockedUser = auth_repository_db_user
    user = MockedUser()
    user1 = MockedUser()

    auth_repository.follow(user, user1)

    mocked_db.session.commit.assert_called_once()
    user.follow.assert_called_once_with(user1)


def test_positive_unfollow_user(auth_repository_db_user):
    auth_repository, mocked_db, MockedUser = auth_repository_db_user
    user = MockedUser()
    user1 = MockedUser()

    auth_repository.follow(user, user1)
    auth_repository.unfollow(user, user1)

    user.follow.assert_called_once_with(user1)
    user.unfollow.assert_called_once_with(user1)
    assert mocked_db.session.commit.call_count == 2
