import pytest
from http import HTTPStatus

from app.models.song import Song
from app.common.messages import (
    PLAYLIST_NOT_FOUND,
    UNAUTHORIZED_TO_DELETE_PLAYLIST,
    UNAUTHORIZED_TO_UPDATE_PLAYLIST,
)

NUM_SONGS = 10
REGISTER_USER_URL = "/auth/register"
LOGIN_USER_URL = "/auth/login"
CREATE_PLAYLIST_URL = "/playlist/create"
UPDATE_PLAYLIST_URL = "/playlist/update/1"
DELETE_PLAYLIST_URL = "/playlist/delete/1"
GET_PLAYLIST_BY_ID_URL = "/playlist/get-by-id/1"
TEST_UPDATED_TEXT = "test updated"


USER_DATA = {
    "username": f"test",
    "email": f"test@test.com",
    "password": f"test",
}


def create_playlist(client, token):
    data = {"title": "test"}
    client.post(
        CREATE_PLAYLIST_URL,
        headers={"Authorization": f"Bearer {token}"},
        data=data,
    )


@pytest.fixture
def register(client):
    client.post(REGISTER_USER_URL, json=USER_DATA)

    yield client


@pytest.fixture
def login(register):
    client = register
    response = client.post(LOGIN_USER_URL, json=USER_DATA)
    token = response.json["token"]
    yield client, token


@pytest.fixture
def songs(db):
    songs_ = []
    for i in range(NUM_SONGS):
        word = f"test-{i}"
        song = Song(
            title=word,
            song_url=word,
            small_thumbnail_url=word,
            large_thumbnail_url=word,
            user_id=1,
        )

        db.session.add(song)
        songs_.append(song)

    db.session.commit()

    yield songs_


def test_positive_create_playlist(login):
    client, token = login

    data = {"title": "test"}
    response = client.post(
        CREATE_PLAYLIST_URL,
        headers={"Authorization": f"Bearer {token}"},
        data=data,
    )
    assert response.status_code == HTTPStatus.CREATED


def test_negative_create_playlist_required_title(login):
    client, token = login

    data = {}
    response = client.post(
        CREATE_PLAYLIST_URL,
        headers={"Authorization": f"Bearer {token}"},
        data=data,
    )
    data = response.json
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data["message"] == "title is required"


def test_positive_update_playlist(login):
    client, token = login

    create_playlist(client, token)

    updated_data = {"title": TEST_UPDATED_TEXT}
    response = client.put(
        UPDATE_PLAYLIST_URL,
        headers={"Authorization": f"Bearer {token}"},
        data=updated_data,
    )

    assert response.status_code == HTTPStatus.OK


def test_negative_update_playlist_unauthorized(login):
    client, token = login

    user2_data = {
        "username": "test2",
        "email": "test2@test.com",
        "password": "test2",
    }
    client.post(REGISTER_USER_URL, json=user2_data)
    response = client.post(LOGIN_USER_URL, json=user2_data)
    token2 = response.json["token"]

    create_playlist(client, token)

    updated_data = {"title": TEST_UPDATED_TEXT}
    response = client.put(
        UPDATE_PLAYLIST_URL,
        headers={"Authorization": f"Bearer {token2}"},
        data=updated_data,
    )

    data = response.json
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert data["message"] == UNAUTHORIZED_TO_UPDATE_PLAYLIST


def test_negative_update_playlist_not_found(login):
    client, token = login

    updated_data = {"title": TEST_UPDATED_TEXT}
    response = client.put(
        UPDATE_PLAYLIST_URL,
        headers={"Authorization": f"Bearer {token}"},
        data=updated_data,
    )

    data = response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["message"] == PLAYLIST_NOT_FOUND


def test_positive_delete_playlist(login):
    client, token = login

    create_playlist(client, token)

    response = client.delete(
        DELETE_PLAYLIST_URL,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK


def test_negative_delete_playlist_unauthorized(login):
    client, token = login

    user2_data = {
        "username": "test2",
        "email": "test2@test.com",
        "password": "test2",
    }
    client.post(REGISTER_USER_URL, json=user2_data)
    response = client.post(LOGIN_USER_URL, json=user2_data)
    token2 = response.json["token"]

    create_playlist(client, token)

    response = client.delete(
        DELETE_PLAYLIST_URL, headers={"Authorization": f"Bearer {token2}"}
    )

    data = response.json
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert data["message"] == UNAUTHORIZED_TO_DELETE_PLAYLIST


def test_negative_delete_playlist_not_found(login):
    client, token = login

    response = client.delete(
        DELETE_PLAYLIST_URL, headers={"Authorization": f"Bearer {token}"}
    )

    data = response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["message"] == PLAYLIST_NOT_FOUND


def test_positive_playlist_get_all_default(login):
    client, token = login

    for _ in range(NUM_SONGS):
        create_playlist(client, token)

    response = client.get(
        "/playlist/get-all", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == NUM_SONGS


def test_positive_playlist_get_all_with_pagination(login):
    client, token = login

    for _ in range(NUM_SONGS):
        create_playlist(client, token)

    response = client.get(
        "/playlist/get-all?take=5&skip=5", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 5


def test_positive_playlist_get_all_empty(login):
    client, token = login

    response = client.get(
        "/playlist/get-all", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 0


def test_positive_playlist_get_by_id(login):
    client, token = login

    create_playlist(client, token)

    response = client.get(
        GET_PLAYLIST_BY_ID_URL, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["title"] == "test"


def test_negative_playlist_get_by_id_not_found(login):
    client, token = login

    response = client.get(
        GET_PLAYLIST_BY_ID_URL, headers={"Authorization": f"Bearer {token}"}
    )

    data = response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["message"] == PLAYLIST_NOT_FOUND


def test_positive_playlist_add_song(login, songs):
    client, token = login

    create_playlist(client, token)

    for song in songs:
        response = client.post(
            f"/playlist/add-song/1/{song.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.OK


def test_positive_playlist_remove_song(login, songs):
    client, token = login

    create_playlist(client, token)

    for song in songs:
        response = client.post(
            f"/playlist/add-song/1/{song.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.OK

    for song in songs:
        response = client.post(
            f"/playlist/remove-song/1/{song.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.OK


def test_positive_playlist_get_by_id_with_songs_default_params(login, songs):
    client, token = login

    create_playlist(client, token)

    for song in songs:
        response = client.post(
            f"/playlist/add-song/1/{song.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.OK

    response = client.get(
        GET_PLAYLIST_BY_ID_URL, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["songs"]) == len(songs)


def test_positive_playlist_get_by_id_with_songs_with_pagination(login, songs):
    client, token = login

    create_playlist(client, token)

    for song in songs:
        response = client.post(
            f"/playlist/add-song/1/{song.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.OK

    response = client.get(
        "/playlist/get-by-id/1?take=5&skip=5",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["songs"]) == 5
