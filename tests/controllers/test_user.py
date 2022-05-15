import pytest
from unittest import mock

from app.controllers.user import UserController
from app.common.exceptions import NotFoundException
from app.common.messages import USER_ID_REQUIRED, USER_NOT_FOUND


@pytest.fixture
def mocked_user_service():
    with mock.patch("app.controllers.user.UserService") as MockedUserService:
        yield MockedUserService


@pytest.fixture
def mocked_jsonify():
    with mock.patch("app.controllers.user.jsonify") as mocked_jsonify_:
        yield mocked_jsonify_


def test_positive_follow(mocked_user_service):
    request = mock.MagicMock()
    request.args.get.return_value = 2

    current_user = mock.MagicMock()
    current_user.id = 1

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.follow(request, current_user)

    mocked_user_service.return_value.follow.assert_called_once_with(current_user, 2)
    request.args.get.assert_called_once_with("user_id", None, int)


def test_negative_follow_user_id_not_provided(mocked_user_service, mocked_jsonify):
    request = mock.MagicMock()
    request.args.get.return_value = None

    current_user = mock.MagicMock()
    current_user.id = 1

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.follow(request, current_user)

    mocked_jsonify.assert_called_once_with({"message": USER_ID_REQUIRED})
    request.args.get.assert_called_once_with("user_id", None, int)


def test_negative_follow_user_not_found(mocked_user_service, mocked_jsonify):
    request = mock.MagicMock()
    request.args.get.return_value = 2

    current_user = mock.MagicMock()
    current_user.id = 1
    err = NotFoundException(USER_NOT_FOUND)
    mocked_user_service.return_value.follow.side_effect = err

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.follow(request, current_user)

    mocked_user_service.return_value.follow.assert_called_once_with(current_user, 2)
    request.args.get.assert_called_once_with("user_id", None, int)
    mocked_jsonify.assert_called_once_with(err.to_dict())


def test_positive_unfollow(mocked_user_service):
    request = mock.MagicMock()
    request.args.get.return_value = 2

    current_user = mock.MagicMock()
    current_user.id = 1

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.unfollow(request, current_user)

    mocked_user_service.return_value.unfollow.assert_called_once_with(current_user, 2)
    request.args.get.assert_called_once_with("user_id", None, int)


def test_negative_unfollow_user_id_not_provided(mocked_user_service, mocked_jsonify):
    request = mock.MagicMock()
    request.args.get.return_value = None

    current_user = mock.MagicMock()
    current_user.id = 1

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.unfollow(request, current_user)

    mocked_jsonify.assert_called_once_with({"message": USER_ID_REQUIRED})
    request.args.get.assert_called_once_with("user_id", None, int)


def test_negative_unfollow_user_not_found(mocked_user_service, mocked_jsonify):
    request = mock.MagicMock()
    request.args.get.return_value = 2

    current_user = mock.MagicMock()
    current_user.id = 1
    err = NotFoundException(USER_NOT_FOUND)
    mocked_user_service.return_value.unfollow.side_effect = err

    user_controller = UserController(mocked_user_service.return_value)
    user_controller.unfollow(request, current_user)

    mocked_user_service.return_value.unfollow.assert_called_once_with(current_user, 2)
    request.args.get.assert_called_once_with("user_id", None, int)
    mocked_jsonify.assert_called_once_with(err.to_dict())


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
