import pytest
from http import HTTPStatus

USER_DATA = {
    "username": f"test",
    "email": f"test@test.com",
    "password": f"test",
}


@pytest.fixture
def register(client):
    client.post("/auth/register", json=USER_DATA)

    yield client


@pytest.fixture
def login(register):
    client = register
    response = client.post("/auth/login", json=USER_DATA)
    token = response.json["token"]
    yield client, token


def test_negative_get_song_by_id_not_found(login):
    client, token = login
    response = client.get(
        "/song/get-by-id/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_positive_get_all_song(login):
    client, token = login
    response = client.get("/song/get-all", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
