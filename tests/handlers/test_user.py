import pytest
from http import HTTPStatus

from app.common.messages import USER_ID_REQUIRED, USER_NOT_FOUND

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"

NUM_USERS = 10


def create_data(i):
    return {
        "username": f"test{i}",
        "email": f"test{i}@test.com",
        "password": f"test{i}",
    }


@pytest.fixture
def register(client):
    for i in range(1, NUM_USERS + 1):
        client.post(REGISTER_URL, json=create_data(i))


@pytest.fixture
def login(client, register):
    tokens = []
    for i in range(1, NUM_USERS + 1):
        response = client.post(LOGIN_URL, json=create_data(i))
        tokens.append(response.json["token"])

    yield tokens


def test_positive_follow(client, login):
    tokens = login
    for token in tokens[1:]:
        response = client.post(
            f"/user/follow?user_id=1",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == HTTPStatus.OK


def test_negative_follow_user_id_not_provided(client, login):
    tokens = login
    for token in tokens[1:]:
        response = client.post(
            f"/user/follow",
            headers={"Authorization": f"Bearer {token}"},
        )
        data = response.json

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data["message"] == USER_ID_REQUIRED


def test_negative_follow_user_target_not_found(client, login):
    tokens = login
    for token in tokens[1:]:
        response = client.post(
            f"/user/follow?user_id=100",
            headers={"Authorization": f"Bearer {token}"},
        )
        data = response.json

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert data["message"] == USER_NOT_FOUND


def test_positive_unfollow(client, login):
    tokens = login
    for token in tokens[1:]:
        response = client.post(
            f"/user/unfollow?user_id=1",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == HTTPStatus.OK


def test_negative_unfollow_user_id_not_provided(client, login):
    tokens = login
    for token in tokens[1:]:
        response = client.post(
            f"/user/unfollow",
            headers={"Authorization": f"Bearer {token}"},
        )
        data = response.json

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data["message"] == USER_ID_REQUIRED


def test_negative_unfollow_user_target_not_found(client, login):
    tokens = login
    for token in tokens[1:]:
        response = client.post(
            f"/user/unfollow?user_id=100",
            headers={"Authorization": f"Bearer {token}"},
        )
        data = response.json

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert data["message"] == USER_NOT_FOUND


def test_positive_get_followers_default_take_skip(client, login):
    tokens = login
    for token in tokens[1:]:
        client.post(
            f"/user/follow?user_id=1",
            headers={"Authorization": f"Bearer {token}"},
        )

    response = client.get(
        "/user/get-followers", headers={"Authorization": f"Bearer {tokens[0]}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["followers"]) == NUM_USERS - 1


def test_positive_get_followers_with_take_skip(client, login):
    tokens = login
    for token in tokens[1:]:
        client.post(
            f"/user/follow?user_id=1",
            headers={"Authorization": f"Bearer {token}"},
        )

    response = client.get(
        "/user/get-followers?take=5&skip=0",
        headers={"Authorization": f"Bearer {tokens[0]}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["followers"]) == 5


def test_positive_get_followed_users_default_take_skip(client, login):
    tokens = login
    for i in range(2, NUM_USERS + 1):
        client.post(
            f"/user/follow?user_id={i}",
            headers={"Authorization": f"Bearer {tokens[0]}"},
        )

    response = client.get(
        "/user/get-followed-users", headers={"Authorization": f"Bearer {tokens[0]}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["followed_users"]) == NUM_USERS - 1


def test_positive_get_followed_users_with_take_skip(client, login):
    tokens = login
    for i in range(2, NUM_USERS + 1):
        client.post(
            f"/user/follow?user_id={i}",
            headers={"Authorization": f"Bearer {tokens[0]}"},
        )

    response = client.get(
        "/user/get-followed-users?take=5&skip=0",
        headers={"Authorization": f"Bearer {tokens[0]}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["followed_users"]) == 5


def test_positive_get_songs_by_user_id(client):
    client.post(REGISTER_URL, json=create_data(0))
    response = client.post(LOGIN_URL, json=create_data(0))
    token = response.json["token"]

    response = client.get(
        "/user/get-songs-by-user-id/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
