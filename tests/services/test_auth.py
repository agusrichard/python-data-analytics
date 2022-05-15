import pytest
from unittest import mock
from sqlalchemy.exc import IntegrityError

from app.services.auth import AuthService
from app.common.messages import WRONG_EMAIL_PASSWORD, USER_ALREADY_EXISTS
from app.common.exceptions import BadRequestException, DataAlreadyExists

DATA = {
    "username": "test",
    "email": "test@test.com",
    "password": "test",
}


@mock.patch("app.services.auth.UserRepository")
def test_positive_register(MockedUserRepository):
    auth_service = AuthService(MockedUserRepository.return_value)

    auth_service.register(DATA)

    MockedUserRepository.return_value.create.assert_called_once_with(DATA)


@mock.patch("app.services.auth.UserRepository")
def test_negative_register_user_already_exists(MockedUserRepository):
    MockedUserRepository.return_value.create.side_effect = DataAlreadyExists(
        USER_ALREADY_EXISTS
    )

    with pytest.raises(DataAlreadyExists):
        auth_service = AuthService(MockedUserRepository.return_value)
        auth_service.register(DATA)

    MockedUserRepository.return_value.create.assert_called_once_with(DATA)


@mock.patch("app.services.auth.UserRepository")
def test_positive_login(MockedUserRepository):
    auth_service = AuthService(MockedUserRepository.return_value)
    auth_service.login(DATA)

    MockedUserRepository.return_value.get_by_email.assert_called_once_with(
        DATA["email"]
    )
    MockedUserRepository.return_value.update.assert_called_once()


@mock.patch("app.services.auth.UserRepository")
def test_negative_login_user_not_found(MockedUserRepository):
    MockedUserRepository.return_value.get_by_email.return_value = None

    with pytest.raises(BadRequestException) as e:
        auth_service = AuthService(MockedUserRepository.return_value)
        auth_service.login(DATA)

    assert str(e.value) == WRONG_EMAIL_PASSWORD

    MockedUserRepository.return_value.get_by_email.assert_called_once_with(
        DATA["email"]
    )


@mock.patch("app.services.auth.UserRepository")
def test_negative_login_user_wrong_password(MockedUserRepository):
    MockedUserRepository.return_value.get_by_email.return_value = mock.Mock()
    MockedUserRepository.return_value.get_by_email.return_value.check_password.return_value = (
        False
    )

    auth_service = AuthService(MockedUserRepository.return_value)
    with pytest.raises(BadRequestException) as e:
        auth_service.login(DATA)

    assert str(e.value) == WRONG_EMAIL_PASSWORD

    MockedUserRepository.return_value.get_by_email.assert_called_once_with(
        DATA["email"]
    )
