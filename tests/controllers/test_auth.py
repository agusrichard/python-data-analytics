import pytest
from flask import Request
from unittest import mock
from http import HTTPStatus
from typing import Callable

from app.controllers.auth import AuthController
from app.common.exceptions import BadRequestException, DataAlreadyExists
from app.common.messages import (
    EMAIL_PASSWORD_REQUIRED,
    USER_ALREADY_EXISTS,
    WRONG_EMAIL_PASSWORD,
)
from app.models.user import User
from app.services.auth import AuthService

DATA = {
    "username": "test",
    "email": "test@test.com",
    "password": "test",
}


@pytest.fixture
def mocked_auth_service():
    with mock.patch("app.controllers.auth.AuthService") as MockedAuthService:
        yield MockedAuthService.return_value


@pytest.fixture
def mocked_jsonify():
    with mock.patch("app.controllers.auth.jsonify") as mocked_jsonify_:
        yield mocked_jsonify_


@pytest.fixture
def mocked_request():
    m = mock.MagicMock()
    with mock.patch("app.controllers.auth.request", m) as mocked_request_:
        yield mocked_request_


def test_positive_register_success(
    mocked_auth_service: AuthService, mocked_request: Request
):
    mocked_request.json = DATA
    auth_controller = AuthController(mocked_auth_service)
    _, status_code = auth_controller.register()

    mocked_auth_service.register.assert_called_once_with(DATA)
    assert status_code == HTTPStatus.CREATED


def test_negative_register_user_already_exists(
    mocked_auth_service: AuthService, mocked_request: Request, mocked_jsonify: Callable
):
    err = DataAlreadyExists(USER_ALREADY_EXISTS)
    mocked_auth_service.register.side_effect = err

    mocked_request.json = DATA

    auth_controller = AuthController(mocked_auth_service)
    _, status_code = auth_controller.register()

    mocked_auth_service.register.assert_called_once_with(DATA)
    mocked_jsonify.assert_called_once()
    assert status_code == err.error_code
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_positive_login_user(
    mocked_auth_service: AuthService, mocked_request: Request, mocked_jsonify: Callable
):
    mocked_request.json = DATA

    auth_controller = AuthController(mocked_auth_service.return_value)
    _, status_code = auth_controller.login()

    mocked_auth_service.return_value.login.assert_called_once_with(DATA)
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.OK


def test_negative_login_user_email_password_not_provided(
    mocked_auth_service: AuthService, mocked_request: Request, mocked_jsonify: Callable
):
    mocked_request.json = {}

    auth_controller = AuthController(mocked_auth_service.return_value)
    _, status_code = auth_controller.login()

    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.BAD_REQUEST
    assert mocked_jsonify.call_args_list[0] == mock.call(
        {
            "message": EMAIL_PASSWORD_REQUIRED,
            "error_code": HTTPStatus.BAD_REQUEST,
        }
    )


def test_negative_login_user_not_found(
    mocked_auth_service: AuthService, mocked_request: Request, mocked_jsonify: Callable
):
    err = BadRequestException(WRONG_EMAIL_PASSWORD)
    mocked_auth_service.return_value.login.side_effect = err

    mocked_request.json = DATA

    auth_controller = AuthController(mocked_auth_service.return_value)
    _, status_code = auth_controller.login()

    mocked_jsonify.assert_called_once()
    assert status_code == err.error_code
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_profile(mocked_current_user: User, mocked_jsonify: Callable):

    auth_controller = AuthController(mock.MagicMock())
    _, status_code = auth_controller.profile(mocked_current_user)

    mocked_jsonify.assert_called_once()
    mocked_current_user.to_dict.assert_called_once()
    assert status_code == HTTPStatus.OK
