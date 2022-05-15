import pytest
from unittest import mock

from app.controllers.user import UserController
from app.common.exceptions import BadRequestException
from app.common.messages import USER_NOT_FOUND


@pytest.fixture
def mocked_user_service():
    with mock.patch("app.controllers.user.UserService") as MockedUserService:
        yield MockedUserService


@pytest.fixture
def mocked_jsonify():
    with mock.patch("app.controllers.user.jsonify") as mocked_jsonify_:
        yield mocked_jsonify_


def test_positive_follow(mocked_user_service):
    current_user = mock.MagicMock()
    current_user.id = 1

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.follow(current_user, 2)

    mocked_user_service.return_value.follow.assert_called_once_with(1, 2)


def test_negative_follow_user_not_found(mocked_user_service, mocked_jsonify):
    current_user = mock.MagicMock()
    current_user.id = 1
    mocked_user_service.return_value.follow.side_effect = BadRequestException(
        USER_NOT_FOUND
    )

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.follow(current_user, 2)

    mocked_user_service.return_value.follow.assert_called_once_with(1, 2)


def test_positive_unfollow(mocked_user_service):
    current_user = mock.MagicMock()
    current_user.id = 1

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.unfollow(current_user, 2)

    mocked_user_service.return_value.unfollow.assert_called_once_with(1, 2)


def test_negative_unfollow_user_not_found(mocked_user_service, mocked_jsonify):
    current_user = mock.MagicMock()
    current_user.id = 1
    mocked_user_service.return_value.unfollow.side_effect = BadRequestException(
        USER_NOT_FOUND
    )

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.unfollow(current_user, 2)

    mocked_user_service.return_value.unfollow.assert_called_once_with(1, 2)


def test_positive_get_followers(mocked_user_service, mocked_jsonify):
    request = mock.MagicMock()
    current_user = mock.MagicMock()

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.get_followers(request, current_user)

    mocked_jsonify.assert_called_once()
    assert request.args.get.call_args_list == [
        mock.call("take", 10, int),
        mock.call("skip", 0, int),
    ]


def test_positive_get_followed_users(mocked_user_service, mocked_jsonify):
    request = mock.MagicMock()
    current_user = mock.MagicMock()

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.get_followed_users(request, current_user)

    mocked_jsonify.assert_called_once()
    assert request.args.get.call_args_list == [
        mock.call("take", 10, int),
        mock.call("skip", 0, int),
    ]
