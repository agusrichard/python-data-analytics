import pytest
from unittest import mock

from app.services.user import UserService
from app.common.messages import USER_NOT_FOUND
from app.common.exceptions import NotFoundException


@mock.patch("app.services.user.UserRepository")
def test_positive_follow(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = mock.MagicMock()

    user_service = UserService(MockedUserRepository.return_value)

    user_service.follow(1, 2)

    MockedUserRepository.return_value.follow.assert_called_once()
    MockedUserRepository.return_value.get_by_id.assert_called_once()


@mock.patch("app.services.user.UserRepository")
def test_negative_follow_users_not_found(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = None

    user_service = UserService(MockedUserRepository.return_value)

    with pytest.raises(NotFoundException):
        user_service.follow(1, 2)

    MockedUserRepository.return_value.get_by_id.assert_called_once()


@mock.patch("app.services.user.UserRepository")
def test_positive_unfollow(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = mock.MagicMock()

    user_service = UserService(MockedUserRepository.return_value)

    user_service.unfollow(1, 2)

    MockedUserRepository.return_value.unfollow.assert_called_once()
    MockedUserRepository.return_value.get_by_id.assert_called_once()


@mock.patch("app.services.user.UserRepository")
def test_negative_unfollow_users_not_found(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = None

    user_service = UserService(MockedUserRepository.return_value)

    with pytest.raises(NotFoundException):
        user_service.unfollow(1, 2)

    MockedUserRepository.return_value.get_by_id.assert_called_once()


@mock.patch("app.services.user.UserRepository")
def test_positive_get_followers(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = mock.MagicMock()
    MockedUserRepository.return_value.get_by_id.return_value.get_followers.return_value = [
        mock.MagicMock() for _ in range(3)
    ]

    user_service = UserService(MockedUserRepository.return_value)

    followers = user_service.get_followers(1)

    assert len(followers) == 3
    MockedUserRepository.return_value.get_by_id.assert_called_once_with(1)
    MockedUserRepository.return_value.get_by_id.return_value.get_followers.assert_called_once()


@mock.patch("app.services.user.UserRepository")
def test_positive_get_followers_with_take_skip(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = mock.MagicMock()
    MockedUserRepository.return_value.get_by_id.return_value.get_followers.return_value = [
        mock.MagicMock() for _ in range(10)
    ]

    user_service = UserService(MockedUserRepository.return_value)

    followers = user_service.get_followers(1, 10, 10)

    assert len(followers) == 10
    MockedUserRepository.return_value.get_by_id.assert_called_once_with(1)
    MockedUserRepository.return_value.get_by_id.return_value.get_followers.assert_called_once_with(
        10, 10
    )


@mock.patch("app.services.user.UserRepository")
def test_negative_get_followers_user_not_found(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = None

    user_service = UserService(MockedUserRepository.return_value)
    with pytest.raises(NotFoundException) as e:
        user_service.get_followers(1)

    assert str(e.value) == USER_NOT_FOUND

    MockedUserRepository.return_value.get_by_id.assert_called_once_with(1)


@mock.patch("app.services.user.UserRepository")
def test_positive_get_followed_users(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = mock.MagicMock()
    MockedUserRepository.return_value.get_by_id.return_value.get_followed_users.return_value = [
        mock.MagicMock() for _ in range(3)
    ]

    user_service = UserService(MockedUserRepository.return_value)

    followed_users = user_service.get_followed_users(1)

    assert len(followed_users) == 3
    MockedUserRepository.return_value.get_by_id.assert_called_once_with(1)
    MockedUserRepository.return_value.get_by_id.return_value.get_followed_users.assert_called_once()


@mock.patch("app.services.user.UserRepository")
def test_positive_get_followed_users_with_take_skip(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = mock.MagicMock()
    MockedUserRepository.return_value.get_by_id.return_value.get_followed_users.return_value = [
        mock.MagicMock() for _ in range(10)
    ]

    user_service = UserService(MockedUserRepository.return_value)

    followed_users = user_service.get_followed_users(1, 10, 10)

    assert len(followed_users) == 10
    MockedUserRepository.return_value.get_by_id.assert_called_once_with(1)
    MockedUserRepository.return_value.get_by_id.return_value.get_followed_users.assert_called_once_with(
        10, 10
    )


@mock.patch("app.services.user.UserRepository")
def test_negative_get_followed_users_user_not_found(MockedUserRepository):
    MockedUserRepository.return_value.get_by_id.return_value = None

    user_service = UserService(MockedUserRepository.return_value)
    with pytest.raises(NotFoundException) as e:
        user_service.get_followed_users(1)

    assert str(e.value) == USER_NOT_FOUND

    MockedUserRepository.return_value.get_by_id.assert_called_once_with(1)
