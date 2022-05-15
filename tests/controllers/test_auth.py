import pytest
from unittest import mock

from app.controllers.auth import AuthController
from app.common.exceptions import BadRequestException, DataAlreadyExists
from app.common.messages import USER_ALREADY_EXISTS, WRONG_EMAIL_PASSWORD

DATA = {
    "username": "test",
    "email": "test@test.com",
    "password": "test",
}


@pytest.fixture
def mocked_auth_service():
    with mock.patch("app.controllers.auth.AuthService") as MockedAuthService:
        yield MockedAuthService


@pytest.fixture
def mocked_jsonify():
    with mock.patch("app.controllers.auth.jsonify") as mocked_jsonify_:
        yield mocked_jsonify_


def test_positive_register_success(mocked_auth_service):
    request = mock.MagicMock()
    request.json = DATA

    auth_controller = AuthController(mocked_auth_service.return_value)
    auth_controller.register(request)

    mocked_auth_service.return_value.register.assert_called_once_with(DATA)


def test_negative_register_user_already_exists(mocked_auth_service, mocked_jsonify):
    mocked_auth_service.return_value.register.side_effect = DataAlreadyExists(
        USER_ALREADY_EXISTS
    )

    request = mock.MagicMock()
    request.json = DATA

    auth_controller = AuthController(mocked_auth_service.return_value)
    auth_controller.register(request)

    mocked_auth_service.return_value.register.assert_called_once_with(DATA)
    mocked_jsonify.assert_called_once()


def test_positive_login_user(mocked_auth_service, mocked_jsonify):
    request = mock.MagicMock()
    request.json = DATA

    auth_controller = AuthController(mocked_auth_service.return_value)
    auth_controller.login(request)

    mocked_auth_service.return_value.login.assert_called_once_with(DATA)
    mocked_jsonify.assert_called_once()


def test_negative_login_user_email_password_not_provided(
    mocked_auth_service, mocked_jsonify
):
    request = mock.MagicMock()
    request.json = {}

    auth_controller = AuthController(mocked_auth_service.return_value)
    auth_controller.login(request)

    mocked_jsonify.assert_called_once()


def test_negative_login_user_not_found(mocked_jsonify, mocked_auth_service):
    mocked_auth_service.return_value.login.side_effect = BadRequestException(
        WRONG_EMAIL_PASSWORD
    )

    request = mock.MagicMock()
    request.json = DATA

    auth_controller = AuthController(mocked_auth_service.return_value)
    auth_controller.login(request)

    mocked_jsonify.assert_called_once()


def test_profile(mocked_jsonify):
    current_user = mock.MagicMock()

    auth_controller = AuthController(mock.MagicMock())
    auth_controller.profile(current_user)

    mocked_jsonify.assert_called_once()
    current_user.to_dict.assert_called_once()
