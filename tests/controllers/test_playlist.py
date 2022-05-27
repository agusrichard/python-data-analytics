import pytest
from unittest import mock
from flask import Request
from http import HTTPStatus
from typing import Callable

from app.models.user import User
from app.services.playlist import PlaylistService
from app.controllers.playlist import PlaylistController
from app.common.exceptions import (
    FieldRequiredException,
    NotFoundException,
    UnauthorizedException,
)
from app.common.messages import (
    PLAYLIST_NOT_FOUND,
    SONG_NOT_FOUND,
    UNAUTHORIZED_TO_DELETE_PLAYLIST,
    UNAUTHORIZED_TO_UPDATE_PLAYLIST,
    UNAUTHORIZED_ADD_SONG_TO_PLAYLIST,
    UNAUTHORIZED_REMOVE_SONG_FROM_PLAYLIST,
)


@pytest.fixture
def mocked_playlist_service():
    with mock.patch(
        "app.controllers.playlist.PlaylistService"
    ) as MockedPlaylistService:
        yield MockedPlaylistService.return_value


@pytest.fixture
def mocked_jsonify():
    with mock.patch("app.controllers.playlist.jsonify") as mocked_jsonify_:
        yield mocked_jsonify_


@pytest.fixture
def mocked_request():
    m = mock.MagicMock()
    with mock.patch("app.controllers.playlist.request", m) as mocked_request_:
        yield mocked_request_


def test_positive_create_playlist(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_current_user: User,
):
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.create(mocked_current_user)

    mocked_request.form.to_dict.assert_called_once()
    mocked_playlist_service.create.assert_called_once()
    assert status_code == HTTPStatus.CREATED


def test_negative_create_playlist_field_required(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = FieldRequiredException("title")
    mocked_playlist_service.create.side_effect = FieldRequiredException("title")

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.create(mocked_current_user)

    mocked_request.form.to_dict.assert_called_once()
    mocked_playlist_service.create.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.BAD_REQUEST
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_positive_update_playlist(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_current_user: User,
):
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.update(mocked_current_user, 1)

    mocked_request.form.to_dict.assert_called_once()
    mocked_playlist_service.update.assert_called_once()
    assert status_code == HTTPStatus.OK


def test_negative_update_playlist_playlist_id_not_provided(
    mocked_playlist_service: PlaylistService,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = FieldRequiredException("playlist_id")
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.update(mocked_current_user, None)

    mocked_playlist_service.update.assert_not_called()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.BAD_REQUEST
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_negative_update_playlist_unauthorized(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = UnauthorizedException(UNAUTHORIZED_TO_UPDATE_PLAYLIST)
    mocked_playlist_service.update.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.update(mocked_current_user, 1)

    mocked_request.form.to_dict.assert_called_once()
    mocked_playlist_service.update.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.UNAUTHORIZED
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_negative_update_playlist_not_found(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = NotFoundException(PLAYLIST_NOT_FOUND)
    mocked_playlist_service.update.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.update(mocked_current_user, 1)

    mocked_request.form.to_dict.assert_called_once()
    mocked_playlist_service.update.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.NOT_FOUND
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_positive_delete_playlist(
    mocked_playlist_service: PlaylistService,
    mocked_current_user: User,
):
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.delete(mocked_current_user, 1)

    mocked_playlist_service.delete.assert_called_once()
    assert status_code == HTTPStatus.OK


def test_negative_delete_playlist_playlist_id_not_provided(
    mocked_playlist_service: PlaylistService,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = FieldRequiredException("playlist_id")
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.delete(mocked_current_user, None)

    mocked_playlist_service.delete.assert_not_called()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.BAD_REQUEST
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_negative_delete_playlist_unauthorized(
    mocked_playlist_service: PlaylistService,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = UnauthorizedException(UNAUTHORIZED_TO_DELETE_PLAYLIST)
    mocked_playlist_service.delete.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.delete(mocked_current_user, 1)

    mocked_playlist_service.delete.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.UNAUTHORIZED
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_negative_delete_playlist_not_found(
    mocked_playlist_service: PlaylistService,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = NotFoundException(PLAYLIST_NOT_FOUND)
    mocked_playlist_service.delete.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.delete(mocked_current_user, 1)

    mocked_playlist_service.delete.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.NOT_FOUND
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_positive_playlist_get_all(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
):
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.get_all()

    mocked_playlist_service.get_all.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert mocked_request.args.get.call_count == 2
    assert status_code == HTTPStatus.OK


def test_positive_playlist_get_by_id(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
    mocked_current_user: User,
):
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.get_by_id(mocked_current_user, 1)

    mocked_playlist_service.get_by_id.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert mocked_request.args.get.call_count == 2
    assert status_code == HTTPStatus.OK


def test_negative_playlist_get_by_id_playlist_id_not_provided(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
):
    err = FieldRequiredException("playlist_id")
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.get_by_id(mocked_request, None)

    mocked_playlist_service.get_by_id.assert_not_called()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.BAD_REQUEST
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_negative_playlist_get_by_id_not_found(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
):
    err = NotFoundException(PLAYLIST_NOT_FOUND)
    mocked_playlist_service.get_by_id.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.get_by_id(mocked_request, 1)

    mocked_playlist_service.get_by_id.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.NOT_FOUND
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_positive_playlist_add_song(
    mocked_playlist_service: PlaylistService,
    mocked_current_user: User,
):
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.add_song(mocked_current_user, 1, 1)

    mocked_playlist_service.add_song.assert_called_once()
    assert status_code == HTTPStatus.OK


def test_negative_playlist_add_song_unauthorized(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
):
    err = UnauthorizedException(UNAUTHORIZED_ADD_SONG_TO_PLAYLIST)
    mocked_playlist_service.add_song.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.add_song(mocked_request, 1, 1)

    mocked_playlist_service.add_song.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.UNAUTHORIZED
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_negative_playlist_add_song_playlist_not_found(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
):
    err = NotFoundException(PLAYLIST_NOT_FOUND)
    mocked_playlist_service.add_song.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.add_song(mocked_request, 1, 1)

    mocked_playlist_service.add_song.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.NOT_FOUND
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_negative_playlist_add_song_song_not_found(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
):
    err = NotFoundException(SONG_NOT_FOUND)
    mocked_playlist_service.add_song.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.add_song(mocked_request, 1, 1)

    mocked_playlist_service.add_song.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.NOT_FOUND
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_positive_playlist_remove_song(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_current_user: User,
):
    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.remove_song(mocked_current_user, 1, 1)

    mocked_playlist_service.remove_song.assert_called_once()
    assert status_code == HTTPStatus.OK


def test_negative_playlist_remove_song_unauthorized(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
):
    err = UnauthorizedException(UNAUTHORIZED_REMOVE_SONG_FROM_PLAYLIST)
    mocked_playlist_service.remove_song.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.remove_song(mocked_request, 1, 1)

    mocked_playlist_service.remove_song.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.UNAUTHORIZED
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_negative_playlist_remove_song_playlist_not_found(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
):
    err = NotFoundException(PLAYLIST_NOT_FOUND)
    mocked_playlist_service.remove_song.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.remove_song(mocked_request, 1, 1)

    mocked_playlist_service.remove_song.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.NOT_FOUND
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())


def test_negative_playlist_remove_song_song_not_found(
    mocked_playlist_service: PlaylistService,
    mocked_request: Request,
    mocked_jsonify: Callable,
):
    err = NotFoundException(SONG_NOT_FOUND)
    mocked_playlist_service.remove_song.side_effect = err

    playlist_controller = PlaylistController(mocked_playlist_service)
    _, status_code = playlist_controller.remove_song(mocked_request, 1, 1)

    mocked_playlist_service.remove_song.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.NOT_FOUND
    assert mocked_jsonify.call_args_list[0] == mock.call(err.to_dict())
