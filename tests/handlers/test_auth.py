from http import HTTPStatus

from app.common.messages import USER_ALREADY_EXISTS

DATA = {
    "username": "test",
    "email": "test@test.com",
    "password": "test",
}

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"
PROFILE_URL = "/auth/profile"


def test_register_success(client):
    response = client.post(REGISTER_URL, json=DATA)

    assert response.status_code == 201


def test_register_user_already_exists(client):
    client.post(REGISTER_URL, json=DATA)
    response = client.post(REGISTER_URL, json=DATA)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json["message"] == USER_ALREADY_EXISTS
    assert response.json["error_code"] == HTTPStatus.CONFLICT


def test_login_success(client):
    client.post(REGISTER_URL, json=DATA)
    response = client.post(LOGIN_URL, json=DATA)
    data = response.json

    assert response.status_code == HTTPStatus.OK
    assert "token" in data
    assert "user" in data


def test_login_email_password_not_provided(client):
    client.post(REGISTER_URL, json=DATA)
    response = client.post(LOGIN_URL, json={})
    data = response.json

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "message" in data
    assert "error_code" in data


def test_login_user_not_found(client):
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
    assert data["message"] == "Wrong email or password"
    assert data["error_code"] == HTTPStatus.BAD_REQUEST


def test_user_profile_success(client):
    client.post(REGISTER_URL, json=DATA)
    response = client.post(LOGIN_URL, json=DATA)
    data = response.json

    response = client.get(
        PROFILE_URL, headers={"Authorization": f"Bearer {data['token']}"}
    )
    data = response.json

    assert response.status_code == HTTPStatus.OK
    assert "email" in data
    assert "username" in data


def test_user_profile_token_not_provided(client):
    response = client.get(PROFILE_URL, headers={"Authorization": f""})
    data = response.json

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert data["message"] == "a valid token is missing"


def test_user_profile_invalid_token(client):
    response = client.get(PROFILE_URL, headers={"Authorization": f"Bearer invalid"})
    data = response.json

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert data["message"] == "token is invalid"
