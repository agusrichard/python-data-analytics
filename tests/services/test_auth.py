import pytest
from unittest import mock

from app.services.auth import AuthService
from app.common.exceptions import BadRequestException

DATA = {
    "username": "test",
    "email": "test@test.com",
    "password": "test",
}


@mock.patch("app.services.auth.AuthRepository")
def test_register(MockedAuthRepository):
    auth_service = AuthService(MockedAuthRepository)

    auth_service.register(DATA)

    MockedAuthRepository.create.assert_called_once_with(DATA)


@mock.patch("app.services.auth.AuthRepository")
def test_login_success(MockedAuthRepository):
    auth_service = AuthService(MockedAuthRepository)
    auth_service.login(DATA)

    MockedAuthRepository.get_by_email.assert_called_once_with(DATA["email"])
    MockedAuthRepository.update.assert_called_once()


@mock.patch("app.services.auth.AuthRepository")
def test_login_user_not_found(MockedAuthRepository):
    MockedAuthRepository.get_by_email.return_value = None

    auth_service = AuthService(MockedAuthRepository)
    with pytest.raises(BadRequestException) as e:
        auth_service.login(DATA)

    assert str(e.value) == "Wrong email or password"

    MockedAuthRepository.get_by_email.assert_called_once_with(DATA["email"])


@mock.patch("app.services.auth.AuthRepository")
def test_login_user_wrong_password(MockedAuthRepository):
    MockedAuthRepository.get_by_email.return_value = mock.Mock()
    MockedAuthRepository.get_by_email.return_value.check_password.return_value = False

    auth_service = AuthService(MockedAuthRepository)
    with pytest.raises(BadRequestException) as e:
        auth_service.login(DATA)

    assert str(e.value) == "Wrong email or password"

    MockedAuthRepository.get_by_email.assert_called_once_with(DATA["email"])
