from http import HTTPStatus
import pytest
from flask import Request
from unittest import mock
from typing import Callable
from app.common.messages import (
    FAILED_TO_UPLOAD,
    UNAUTHORIZED_TO_DELETE_SONG,
    UNAUTHORIZED_TO_UPDATE_SONG,
)

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

SONG_NOT_FOUND_MESSAGE = "song not found"
SONG_ID_REQUIRED_MESSAGE = "song_id is required"


@pytest.fixture
def mocked_song_service():
    with mock.patch("app.controllers.song.SongController") as MockedSongService:
        yield MockedSongService.return_value


@pytest.fixture
def mocked_jsonify():
    with mock.patch("app.controllers.song.jsonify") as mocked_jsonify_:
        yield mocked_jsonify_


@pytest.fixture
def mocked_current_user():
    yield mock.MagicMock()


@pytest.fixture
def mocked_request():
    yield mock.MagicMock()


def test_positive_create_song(
    mocked_song_service: SongService, mocked_request: Request, mocked_current_user: User
):
    song_controller = SongController(mocked_song_service)
    song_controller.create(mocked_request, mocked_current_user)

    mocked_song_service.create.assert_called_once()


def test_negative_create_song_raise_field_required(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_song_service.create.side_effect = FieldRequiredException("title")
    song_controller = SongController(mocked_song_service)
    song_controller.create(mocked_request, mocked_current_user)

    mocked_song_service.create.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": "title is required", "error_code": HTTPStatus.BAD_REQUEST}
    )


def test_negative_create_song_raise_upload_failed(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_song_service.create.side_effect = UploadFailedException()
    song_controller = SongController(mocked_song_service)
    song_controller.create(mocked_request, mocked_current_user)

    mocked_song_service.create.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": FAILED_TO_UPLOAD, "error_code": HTTPStatus.INTERNAL_SERVER_ERROR}
    )


def test_negative_create_song_raise_bad_request(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    message = "test bad request"
    mocked_song_service.create.side_effect = BadRequestException(message)
    song_controller = SongController(mocked_song_service)
    song_controller.create(mocked_request, mocked_current_user)

    mocked_song_service.create.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": message, "error_code": HTTPStatus.BAD_REQUEST}
    )


def test_positive_update_song(
    mocked_song_service: SongService, mocked_request: Request, mocked_current_user: User
):
    song_controller = SongController(mocked_song_service)
    song_controller.update(mocked_current_user, mocked_request, 1)

    mocked_song_service.update.assert_called_once()


def test_positive_update_song_check_request_files(
    mocked_song_service: SongService, mocked_request: Request, mocked_current_user: User
):
    mocked_request.files = {
        "song_file": mock.MagicMock(),
        "small_thumbnail_file": mock.MagicMock(),
        "large_thumbnail_file": mock.MagicMock(),
    }

    song_controller = SongController(mocked_song_service)
    song_controller.update(mocked_current_user, mocked_request, 1)

    mocked_song_service.update.assert_called_once()


def test_negative_update_song_id_required(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
    mocked_current_user: User,
    mocked_request: Request,
):
    song_controller = SongController(mocked_song_service)
    song_controller.update(mocked_current_user, mocked_request, None)

    mocked_song_service.delete.assert_not_called()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_ID_REQUIRED_MESSAGE, "error_code": HTTPStatus.BAD_REQUEST}
    )


def test_negative_update_song_raise_field_required(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_song_service.update.side_effect = UnauthorizedException(
        UNAUTHORIZED_TO_UPDATE_SONG
    )
    song_controller = SongController(mocked_song_service)
    song_controller.update(mocked_current_user, mocked_request, 1)

    mocked_song_service.update.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": UNAUTHORIZED_TO_UPDATE_SONG, "error_code": HTTPStatus.UNAUTHORIZED}
    )


def test_negative_update_song_raise_not_found(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_song_service.update.side_effect = NotFoundException(SONG_NOT_FOUND_MESSAGE)
    song_controller = SongController(mocked_song_service)
    song_controller.update(mocked_current_user, mocked_request, 1)

    mocked_song_service.update.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_NOT_FOUND_MESSAGE, "error_code": HTTPStatus.NOT_FOUND}
    )


def test_negative_update_song_raise_upload_failed(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_song_service.update.side_effect = UploadFailedException()
    song_controller = SongController(mocked_song_service)
    song_controller.update(mocked_current_user, mocked_request, 1)

    mocked_song_service.update.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": FAILED_TO_UPLOAD, "error_code": HTTPStatus.INTERNAL_SERVER_ERROR}
    )


def test_negative_update_song_raise_bad_request(
    mocked_song_service: SongService,
    mocked_request: Request,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    message = "test bad request"
    mocked_song_service.update.side_effect = BadRequestException(message)
    song_controller = SongController(mocked_song_service)
    song_controller.update(mocked_current_user, mocked_request, 1)

    mocked_song_service.update.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": message, "error_code": HTTPStatus.BAD_REQUEST}
    )


def test_positive_delete_song(
    mocked_song_service: SongService,
    mocked_current_user: User,
):
    song_controller = SongController(mocked_song_service)
    song_controller.delete(mocked_current_user, 1)

    mocked_song_service.delete.assert_called_once()


def test_negative_delete_song_id_required(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
    mocked_current_user: User,
):
    song_controller = SongController(mocked_song_service)
    song_controller.delete(mocked_current_user, None)

    mocked_song_service.delete.assert_not_called()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_ID_REQUIRED_MESSAGE, "error_code": HTTPStatus.BAD_REQUEST}
    )


def test_negative_delete_song_raise_unauthorized(
    mocked_song_service: SongService,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_song_service.delete.side_effect = UnauthorizedException(
        UNAUTHORIZED_TO_DELETE_SONG
    )

    song_controller = SongController(mocked_song_service)
    song_controller.delete(mocked_current_user, 1)

    mocked_song_service.delete.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": UNAUTHORIZED_TO_DELETE_SONG, "error_code": HTTPStatus.UNAUTHORIZED}
    )


def test_negative_delete_song_raise_not_found(
    mocked_song_service: SongService,
    mocked_current_user: User,
    mocked_jsonify: Callable,
):
    mocked_song_service.delete.side_effect = NotFoundException(SONG_NOT_FOUND_MESSAGE)
    song_controller = SongController(mocked_song_service)
    song_controller.delete(mocked_current_user, 1)

    mocked_song_service.delete.assert_called_once()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_NOT_FOUND_MESSAGE, "error_code": HTTPStatus.NOT_FOUND}
    )


def test_positive_song_get_by_id(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
):
    song_controller = SongController(mocked_song_service)
    song_controller.get_by_id(1)

    mocked_song_service.get_by_id.assert_called_once()
    mocked_jsonify.assert_called_once()


def test_negative_song_get_by_id_song_id_required(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
):
    song_controller = SongController(mocked_song_service)
    song_controller.get_by_id(None)

    mocked_song_service.get_by_id.assert_not_called()
    mocked_jsonify.assert_called_once_with(
        {"message": SONG_ID_REQUIRED_MESSAGE, "error_code": HTTPStatus.BAD_REQUEST}
    )


def test_negative_song_get_by_id_not_found(
    mocked_song_service: SongService,
    mocked_jsonify: Callable,
):
    mocked_song_service.get_by_id.side_effect = NotFoundException(
        SONG_NOT_FOUND_MESSAGE
    )
    song_controller = SongController(mocked_song_service)
    song_controller.get_by_id(1)

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
    song_controller.get_all(mocked_request)

    mocked_song_service.get_all.assert_called_once()
    mocked_jsonify.assert_called_once()
