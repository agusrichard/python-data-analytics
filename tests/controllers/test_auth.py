from unittest import mock

from app.controllers.auth import AuthController
from app.common.messages import USER_ALREADY_EXISTS
from app.common.exceptions import BadRequestException, DataAlreadyExists

DATA = {
    "username": "test",
    "email": "test@test.com",
    "password": "test",
}


@mock.patch("app.controllers.auth.AuthService")
def test_register_success(mocked_auth_service):
    request = mock.MagicMock()
    request.json = DATA

    auth_controller = AuthController(mocked_auth_service)
    auth_controller.register(request)

    mocked_auth_service.register.assert_called_once_with(DATA)


@mock.patch("app.controllers.auth.AuthService")
@mock.patch("app.controllers.auth.jsonify")
def test_register_user_already_exists(mocked_jsonify, mocked_auth_service):
    mocked_auth_service.register.side_effect = DataAlreadyExists(USER_ALREADY_EXISTS)

    request = mock.MagicMock()
    request.json = DATA

    auth_controller = AuthController(mocked_auth_service)
    auth_controller.register(request)

    mocked_auth_service.register.assert_called_once_with(DATA)
    mocked_jsonify.assert_called_once()


@mock.patch("app.controllers.auth.AuthService")
@mock.patch("app.controllers.auth.jsonify")
def test_login_success(mocked_jsonify, mocked_auth_service):
    request = mock.MagicMock()
    request.json = DATA

    auth_controller = AuthController(mocked_auth_service)
    auth_controller.login(request)

    mocked_auth_service.login.assert_called_once_with(DATA)
    mocked_jsonify.assert_called_once()


@mock.patch("app.controllers.auth.AuthService")
@mock.patch("app.controllers.auth.jsonify")
def test_login_user_email_password_not_provided(mocked_jsonify, mocked_auth_service):
    request = mock.MagicMock()
    request.json = {}

    auth_controller = AuthController(mocked_auth_service)
    auth_controller.login(request)

    mocked_jsonify.assert_called_once()


@mock.patch("app.controllers.auth.AuthService")
@mock.patch("app.controllers.auth.jsonify")
def test_login_user_not_found(mocked_jsonify, mocked_auth_service):
    mocked_auth_service.login.side_effect = BadRequestException(
        "Wrong email or password"
    )

    request = mock.MagicMock()
    request.json = DATA

    auth_controller = AuthController(mocked_auth_service)
    auth_controller.login(request)

    mocked_jsonify.assert_called_once()


@mock.patch("app.controllers.auth.jsonify")
def test_profile(mocked_jsonify):
    current_user = mock.MagicMock()

    auth_controller = AuthController(mock.MagicMock())
    auth_controller.profile(current_user)

    mocked_jsonify.assert_called_once()
    current_user.to_dict.assert_called_once()
