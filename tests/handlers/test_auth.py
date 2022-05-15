from http import HTTPStatus

from app.common.messages import (
    TOKEN_INVALID,
    USER_ALREADY_EXISTS,
    VALID_TOKEN_MISSING,
    WRONG_EMAIL_PASSWORD,
    EMAIL_PASSWORD_REQUIRED,
)

DATA = {
    "username": "test",
    "email": "test@test.com",
    "password": "test",
}

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"
PROFILE_URL = "/auth/profile"


def test_positive_register(client):
    response = client.post(REGISTER_URL, json=DATA)

    assert response.status_code == HTTPStatus.CREATED


def test_negative_register_user_already_exists(client):
    client.post(REGISTER_URL, json=DATA)
    response = client.post(REGISTER_URL, json=DATA)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json["message"] == USER_ALREADY_EXISTS
    assert response.json["error_code"] == HTTPStatus.CONFLICT


def test_positive_login(client):
    client.post(REGISTER_URL, json=DATA)
    response = client.post(LOGIN_URL, json=DATA)
    data = response.json

    assert response.status_code == HTTPStatus.OK
    assert "token" in data
    assert "user" in data


def test_negative_login_email_password_not_provided(client):
    client.post(REGISTER_URL, json=DATA)
    response = client.post(LOGIN_URL, json={})
    data = response.json

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data["message"] == EMAIL_PASSWORD_REQUIRED
    assert data["error_code"] == HTTPStatus.BAD_REQUEST


def test_negative_login_user_not_found(client):
    client.post(REGISTER_URL, json=DATA)
    response = client.post(
        LOGIN_URL,
        json={
            "email": "test1@test.com",
            "password": "test",
        },
    )
    data = response.json

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data["message"] == WRONG_EMAIL_PASSWORD
    assert data["error_code"] == HTTPStatus.BAD_REQUEST


def test_positive_user_profile_success(client):
    client.post(REGISTER_URL, json=DATA)
    response = client.post(LOGIN_URL, json=DATA)
    data = response.json

    response = client.get(
        PROFILE_URL, headers={"Authorization": f"Bearer {data['token']}"}
    )
    data = response.json

    assert response.status_code == HTTPStatus.OK
    assert data["username"] == DATA["username"]
    assert data["email"] == DATA["email"]
    assert "id" in data
    assert "bio" in data
    assert "avatar" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "last_login" in data


def test_negative_user_profile_token_not_provided(client):
    response = client.get(PROFILE_URL, headers={"Authorization": f""})
    data = response.json

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert data["message"] == VALID_TOKEN_MISSING


def test_negative_user_profile_invalid_token(client):
    response = client.get(PROFILE_URL, headers={"Authorization": f"Bearer invalid"})
    data = response.json

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert data["message"] == TOKEN_INVALID
