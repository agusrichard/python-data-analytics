import pytest
from flask import Request
from unittest import mock
from http import HTTPStatus
from typing import Callable

from app.models.user import User
from app.services.song import SongService
from app.controllers.song import SongController
from app.common.exceptions import (
    BadRequestException,
    FieldRequiredException,
    NotFoundException,
    UnauthorizedException,
    UploadFailedException,
)

from app.common.messages import (
    FAILED_TO_UPLOAD,
    UNAUTHORIZED_TO_DELETE_SONG,
    UNAUTHORIZED_TO_UPDATE_SONG,
)

SONG_NOT_FOUND_MESSAGE = "song not found"
SONG_ID_REQUIRED_MESSAGE = "song_id is required"


@pytest.fixture
def mocked_song_service():
    with mock.patch("app.controllers.song.SongService") as MockedSongService:
        yield MockedSongService.return_value


@pytest.fixture
def mocked_jsonify():
    with mock.patch("app.controllers.song.jsonify") as mocked_jsonify_:
        yield mocked_jsonify_


@pytest.fixture
def mocked_request():
    m = mock.MagicMock()
    with mock.patch("app.controllers.song.request", m) as mocked_request_:
        yield mocked_request_


def test_positive_create_song(
    mocked_song_service: SongService, mocked_request: Request, mocked_current_user: User
):
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.create(mocked_current_user)

    mocked_song_service.create.assert_called_once()
    assert status_code == HTTPStatus.CREATED
    assert mocked_request.files.get.call_args_list == [
        mock.call("song_file", None),
        mock.call("small_thumbnail_file", None),
        mock.call("large_thumbnail_file", None),
    ]


def test_negative_create_song_raise_field_required(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = FieldRequiredException("title")
    mocked_song_service.create.side_effect = err
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.create(mocked_current_user)

    mocked_song_service.create.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": "title is required", "error_code": HTTPStatus.BAD_REQUEST}
    )
    assert status_code == err.error_code
    assert mocked_request.files.get.call_args_list == [
        mock.call("song_file", None),
        mock.call("small_thumbnail_file", None),
        mock.call("large_thumbnail_file", None),
    ]


def test_negative_create_song_raise_upload_failed(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = UploadFailedException()
    mocked_song_service.create.side_effect = err
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.create(mocked_current_user)

    mocked_song_service.create.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": FAILED_TO_UPLOAD, "error_code": HTTPStatus.INTERNAL_SERVER_ERROR}
    )
    assert status_code == err.error_code
    assert mocked_request.files.get.call_args_list == [
        mock.call("song_file", None),
        mock.call("small_thumbnail_file", None),
        mock.call("large_thumbnail_file", None),
    ]


def test_negative_create_song_raise_bad_request(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    message = "test bad request"
    err = BadRequestException(message)
    mocked_song_service.create.side_effect = err
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.create(mocked_current_user)

    mocked_song_service.create.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": message, "error_code": HTTPStatus.BAD_REQUEST}
    )
    assert status_code == err.error_code
    assert mocked_request.files.get.call_args_list == [
        mock.call("song_file", None),
        mock.call("small_thumbnail_file", None),
        mock.call("large_thumbnail_file", None),
    ]


def test_positive_update_song(
    mocked_song_service: SongService, mocked_request: Request, mocked_current_user: User
):
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.update(mocked_current_user, 1)

    mocked_song_service.update.assert_called_once()
    mocked_request.files.items.assert_called_once()
    assert status_code == HTTPStatus.OK


def test_positive_update_song_check_request_files(
    mocked_song_service: SongService, mocked_request: Request, mocked_current_user: User
):
    mocked_request.files = {
        "song_file": mock.MagicMock(),
        "small_thumbnail_file": mock.MagicMock(),
        "large_thumbnail_file": mock.MagicMock(),
    }

    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.update(mocked_current_user, 1)

    mocked_song_service.update.assert_called_once()
    assert status_code == HTTPStatus.OK


def test_negative_update_song_id_required(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
    mocked_current_user: User,
    mocked_request: Request,
):
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.update(mocked_current_user, None)

    mocked_song_service.delete.assert_not_called()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_ID_REQUIRED_MESSAGE, "error_code": HTTPStatus.BAD_REQUEST}
    )
    mocked_request.files.items.assert_not_called()
    assert status_code == HTTPStatus.BAD_REQUEST


def test_negative_update_song_raise_field_required(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = UnauthorizedException(UNAUTHORIZED_TO_UPDATE_SONG)
    mocked_song_service.update.side_effect = err
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.update(mocked_current_user, 1)

    mocked_song_service.update.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": UNAUTHORIZED_TO_UPDATE_SONG, "error_code": HTTPStatus.UNAUTHORIZED}
    )
    mocked_request.files.items.assert_called_once()
    assert status_code == err.error_code


def test_negative_update_song_raise_not_found(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = NotFoundException(SONG_NOT_FOUND_MESSAGE)
    mocked_song_service.update.side_effect = err
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.update(mocked_current_user, 1)

    mocked_song_service.update.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_NOT_FOUND_MESSAGE, "error_code": HTTPStatus.NOT_FOUND}
    )
    mocked_request.files.items.assert_called_once()
    assert status_code == err.error_code


def test_negative_update_song_raise_upload_failed(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = UploadFailedException()
    mocked_song_service.update.side_effect = err
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.update(mocked_current_user, 1)

    mocked_song_service.update.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": FAILED_TO_UPLOAD, "error_code": HTTPStatus.INTERNAL_SERVER_ERROR}
    )
    mocked_request.files.items.assert_called_once()
    assert status_code == err.error_code


def test_negative_update_song_raise_bad_request(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    message = "test bad request"
    err = BadRequestException(message)
    mocked_song_service.update.side_effect = err
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.update(mocked_current_user, 1)

    mocked_song_service.update.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": message, "error_code": HTTPStatus.BAD_REQUEST}
    )
    mocked_request.files.items.assert_called_once()
    assert status_code == err.error_code


def test_positive_delete_song(
    mocked_song_service: SongService,
    mocked_current_user: User,
):
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.delete(mocked_current_user, 1)

    mocked_song_service.delete.assert_called_once()
    assert status_code == HTTPStatus.OK


def test_negative_delete_song_id_required(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
    mocked_current_user: User,
):
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.delete(mocked_current_user, None)

    mocked_song_service.delete.assert_not_called()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_ID_REQUIRED_MESSAGE, "error_code": HTTPStatus.BAD_REQUEST}
    )
    assert status_code == HTTPStatus.BAD_REQUEST


def test_negative_delete_song_raise_unauthorized(
    mocked_song_service: SongService,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = UnauthorizedException(UNAUTHORIZED_TO_DELETE_SONG)
    mocked_song_service.delete.side_effect = err

    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.delete(mocked_current_user, 1)

    mocked_song_service.delete.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": UNAUTHORIZED_TO_DELETE_SONG, "error_code": HTTPStatus.UNAUTHORIZED}
    )
    assert status_code == err.error_code


def test_negative_delete_song_raise_not_found(
    mocked_song_service: SongService,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    err = NotFoundException(SONG_NOT_FOUND_MESSAGE)
    mocked_song_service.delete.side_effect = err
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.delete(mocked_current_user, 1)

    mocked_song_service.delete.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_NOT_FOUND_MESSAGE, "error_code": HTTPStatus.NOT_FOUND}
    )
    assert status_code == err.error_code


def test_positive_song_get_by_id(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
    mocked_current_user: User,
):
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.get_by_id(mocked_current_user, 1)

    mocked_song_service.get_by_id.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.OK


def test_negative_song_get_by_id_song_id_required(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
    mocked_current_user: User,
):
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.get_by_id(mocked_current_user, None)

    mocked_song_service.get_by_id.assert_not_called()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_ID_REQUIRED_MESSAGE, "error_code": HTTPStatus.BAD_REQUEST}
    )
    assert status_code == HTTPStatus.BAD_REQUEST


def test_negative_song_get_by_id_not_found(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
    mocked_current_user: User,
):
    err = NotFoundException(SONG_NOT_FOUND_MESSAGE)
    mocked_song_service.get_by_id.side_effect = err
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.get_by_id(mocked_current_user, 1)

    mocked_song_service.get_by_id.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_NOT_FOUND_MESSAGE, "error_code": HTTPStatus.NOT_FOUND}
    )


def test_positive_song_get_all(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
    mocked_request: Request,
):
    song_controller = SongController(mocked_song_service)
    _, status_code = song_controller.get_all(mocked_request)

    mocked_song_service.get_all.assert_called_once()
    mocked_jsonify.assert_called_once()
    assert status_code == HTTPStatus.OK
    assert mocked_request.args.get.call_args_list == [
        mock.call("take", 10, int),
        mock.call("skip", 0, int),
    ]
