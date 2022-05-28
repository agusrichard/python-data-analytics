import pytest
from unittest import mock
from flask import Request
from typing import Callable
from http import HTTPStatus

from app.models.user import User
from app.services.user import UserService
from app.controllers.user import UserController
from app.common.exceptions import NotFoundException
from app.common.messages import USER_ID_REQUIRED, USER_NOT_FOUND


@pytest.fixture
def mocked_user_service():
    with mock.patch("app.controllers.user.UserService") as MockedUserService:
        yield MockedUserService.return_value


@pytest.fixture
def mocked_jsonify():
    with mock.patch("app.controllers.user.jsonify") as mocked_jsonify_:
        yield mocked_jsonify_


@pytest.fixture
def mocked_request():
    m = mock.MagicMock()
    with mock.patch("app.controllers.user.request", m) as mocked_request_:
        yield mocked_request_


def test_positive_follow(
    mocked_user_service: UserService, mocked_request: Request, mocked_current_user: User
):
    mocked_request.args.get.return_value = 2

    mocked_current_user.id = 1

    user_controller = UserController(mocked_user_service)
    _, status_code = user_controller.follow(mocked_current_user)

    mocked_user_service.follow.assert_called_once_with(mocked_current_user, 2)
    mocked_request.args.get.assert_called_once_with("user_id", None, int)
    assert status_code == HTTPStatus.OK


def test_negative_follow_user_id_not_provided(
    mocked_user_service: UserService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_request.args.get.return_value = None
    mocked_current_user.id = 1

    user_controller = UserController(mocked_user_service)
    _, status_code = user_controller.follow(mocked_current_user)

    mocked_jsonify.assert_called_once_with({"message": USER_ID_REQUIRED})
    mocked_request.args.get.assert_called_once_with("user_id", None, int)
    assert status_code == HTTPStatus.BAD_REQUEST


def test_negative_follow_user_not_found(
    mocked_user_service: UserService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_request.args.get.return_value = 2
    mocked_current_user.id = 1
    err = NotFoundException(USER_NOT_FOUND)
    mocked_user_service.follow.side_effect = err

    user_controller = UserController(mocked_user_service)
    _, status_code = user_controller.follow(mocked_current_user)

    mocked_user_service.follow.assert_called_once_with(mocked_current_user, 2)
    mocked_request.args.get.assert_called_once_with("user_id", None, int)
    mocked_jsonify.assert_called_once_with(err.to_dict())
    assert status_code == err.error_code


def test_positive_unfollow(
    mocked_user_service: UserService,
    mocked_request: Request,
    mocked_current_user: User,
):
    mocked_request.args.get.return_value = 2
    mocked_current_user.id = 1

    user_controller = UserController(mocked_user_service)
    _, status_code = user_controller.unfollow(mocked_current_user)

    mocked_user_service.unfollow.assert_called_once_with(mocked_current_user, 2)
    mocked_request.args.get.assert_called_once_with("user_id", None, int)
    assert status_code == HTTPStatus.OK


def test_negative_unfollow_user_id_not_provided(
    mocked_user_service: UserService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_request.args.get.return_value = None
    mocked_current_user.id = 1

    user_controller = UserController(mocked_user_service)
    _, status_code = user_controller.unfollow(mocked_current_user)

    mocked_jsonify.assert_called_once_with({"message": USER_ID_REQUIRED})
    mocked_request.args.get.assert_called_once_with("user_id", None, int)
    assert status_code == HTTPStatus.BAD_REQUEST


def test_negative_unfollow_user_not_found(
    mocked_user_service: UserService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_request.args.get.return_value = 2
    mocked_current_user.id = 1
    err = NotFoundException(USER_NOT_FOUND)
    mocked_user_service.unfollow.side_effect = err

    user_controller = UserController(mocked_user_service)
    _, status_code = user_controller.unfollow(mocked_current_user)

    mocked_user_service.unfollow.assert_called_once_with(mocked_current_user, 2)
    mocked_request.args.get.assert_called_once_with("user_id", None, int)
    mocked_jsonify.assert_called_once_with(err.to_dict())
    assert status_code == err.error_code


def test_positive_get_followers(
    mocked_user_service: UserService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    take, skip = 10, 0
    user_controller = UserController(mocked_user_service)
    _, status_code = user_controller.get_followers(mocked_current_user)

    mocked_jsonify.assert_called_once()
    mocked_current_user.get_followers.assert_called_once()
    assert status_code == HTTPStatus.OK
    assert mocked_request.args.get.call_args_list == [
        mock.call("take", take, int),
        mock.call("skip", skip, int),
    ]


def test_positive_get_followed_users(
    mocked_user_service: UserService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    take, skip = 10, 0
    user_controller = UserController(mocked_user_service)
    _, status_code = user_controller.get_followed_users(mocked_current_user)

    mocked_jsonify.assert_called_once()
    mocked_current_user.get_followed_users.assert_called_once()
    assert status_code == HTTPStatus.OK
    assert mocked_request.args.get.call_args_list == [
        mock.call("take", take, int),
        mock.call("skip", skip, int),
    ]


def test_positive_get_songs_by_user_id(
    mocked_user_service: UserService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    user_id = 1
    take, skip = 10, 0
    user_controller = UserController(mocked_user_service)
    user_controller.get_songs(mocked_current_user, user_id)

    mocked_jsonify.assert_called_once()
    mocked_user_service.get_songs.assert_called_once()
    assert mocked_request.args.get.call_args_list == [
        mock.call("take", take, int),
        mock.call("skip", skip, int),
    ]


def test_negative_get_songs_by_user_id_user_not_found(
    mocked_user_service: UserService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    take, skip = 10, 0
    err = NotFoundException(USER_NOT_FOUND)
    mocked_user_service.return_value.get_songs.side_effect = err

    user_controller = UserController(mocked_user_service.return_value)
    _, status_code = user_controller.get_songs(mocked_current_user, 1)

    mocked_user_service.return_value.get_songs.assert_called_once()
    mocked_jsonify.assert_called_once_with(err.to_dict())
    assert status_code == err.error_code
    assert mocked_request.args.get.call_args_list == [
        mock.call("take", take, int),
        mock.call("skip", skip, int),
    ]
