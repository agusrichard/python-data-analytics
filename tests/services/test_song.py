import pytest
from unittest import mock
from typing import Callable

from app.services.song import SongService
from app.repositories.song import SongRepository
from app.common.exceptions import (
    NotFoundException,
    UploadFailedException,
    FieldRequired,
)


@pytest.fixture
def mocked_song_repository():
    with mock.patch("app.services.song.SongRepository") as MockedSongRepository:
        yield MockedSongRepository.return_value


@pytest.fixture
def mocked_upload_file():
    yield mock.MagicMock()


@pytest.fixture
def mocked_renaming_file():
    with mock.patch("app.services.song.renaming_file") as mocked_renaming_file_:
        yield mocked_renaming_file_


def test_positive_create_song(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
    mocked_renaming_file: Callable,
):
    song_service = SongService(mocked_song_repository, mocked_upload_file)

    data = {
        "title": "test",
    }
    files = {
        "song_file": mock.MagicMock(),
        "small_thumbnail_file": mock.MagicMock(),
        "large_thumbnail_file": mock.MagicMock(),
    }

    song_service.create(files, data)

    mocked_song_repository.create.assert_called_once()
    assert mocked_renaming_file.call_count == 3
    assert mocked_upload_file.call_count == 3


def test_negative_create_song_title_required(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
    mocked_renaming_file: Callable,
):
    song_service = SongService(mocked_song_repository, mocked_upload_file)

    data = {}
    files = {
        "song_file": mock.MagicMock(),
        "small_thumbnail_file": mock.MagicMock(),
        "large_thumbnail_file": mock.MagicMock(),
    }

    with pytest.raises(FieldRequired) as e:
        song_service.create(files, data)

    assert str(e.value) == "title is required"
    mocked_song_repository.assert_not_called()
    mocked_upload_file.assert_not_called()
    mocked_renaming_file.assert_not_called()


def test_negative_create_song_song_file_required(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
    mocked_renaming_file: Callable,
):
    song_service = SongService(mocked_song_repository, mocked_upload_file)

    data = {
        "title": "test",
    }
    files = {}

    with pytest.raises(FieldRequired) as e:
        song_service.create(files, data)

    assert str(e.value) == "song_file is required"
    mocked_song_repository.assert_not_called()
    mocked_upload_file.assert_not_called()
    mocked_renaming_file.assert_not_called()


def test_negative_create_song_upload_raise_exception(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
    mocked_renaming_file: Callable,
):
    mocked_upload_file.side_effect = UploadFailedException()

    song_service = SongService(mocked_song_repository, mocked_upload_file)

    data = {
        "title": "test",
    }
    files = {
        "song_file": mock.MagicMock(),
        "small_thumbnail_file": mock.MagicMock(),
        "large_thumbnail_file": mock.MagicMock(),
    }

    with pytest.raises(UploadFailedException):
        song_service.create(files, data)

    mocked_song_repository.assert_not_called()
    assert mocked_renaming_file.call_count == 1
    assert mocked_upload_file.call_count == 1


def test_positive_update_song(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
    mocked_renaming_file: Callable,
):
    song_service = SongService(mocked_song_repository, mocked_upload_file)

    data = {
        "title": "test",
    }
    files = {
        "song_file": mock.MagicMock(),
        "small_thumbnail_file": mock.MagicMock(),
        "large_thumbnail_file": mock.MagicMock(),
    }

    song_service.update(1, files, data)

    mocked_song_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.update.assert_called_once()
    assert mocked_renaming_file.call_count == 3
    assert mocked_upload_file.call_count == 3


def test_negative_update_song_not_found(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
    mocked_renaming_file: Callable,
):
    mocked_song_repository.get_by_id.return_value = None

    song_service = SongService(mocked_song_repository, mocked_upload_file)

    data = {
        "title": "test",
    }
    files = {
        "song_file": mock.MagicMock(),
        "small_thumbnail_file": mock.MagicMock(),
        "large_thumbnail_file": mock.MagicMock(),
    }

    with pytest.raises(NotFoundException):
        song_service.update(1, files, data)

    mocked_song_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.update.assert_not_called()
    mocked_renaming_file.assert_not_called()
    mocked_upload_file.assert_not_called()


def test_negative_update_song_upload_raise_exception(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
    mocked_renaming_file: Callable,
):
    mocked_upload_file.side_effect = UploadFailedException()

    song_service = SongService(mocked_song_repository, mocked_upload_file)

    data = {
        "title": "test",
    }
    files = {
        "song_file": mock.MagicMock(),
        "small_thumbnail_file": mock.MagicMock(),
        "large_thumbnail_file": mock.MagicMock(),
    }

    with pytest.raises(UploadFailedException):
        song_service.update(1, files, data)

    mocked_song_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.update.assert_not_called()
    assert mocked_renaming_file.call_count == 1
    assert mocked_upload_file.call_count == 1


def test_positive_delete(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
):
    song_service = SongService(mocked_song_repository, mocked_upload_file)

    song_service.delete(1)

    mocked_song_repository.delete.assert_called_once()


def test_negative_delete_song_not_found(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
):
    mocked_song_repository.get_by_id.return_value = None

    song_service = SongService(mocked_song_repository, mocked_upload_file)

    with pytest.raises(NotFoundException):
        song_service.delete(1)

    mocked_song_repository.get_by_id.assert_called_once()
    mocked_song_repository.delete.assert_not_called()


def test_positive_get_by_id(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
):
    song_service = SongService(mocked_song_repository, mocked_upload_file)

    song_service.get_by_id(1)

    mocked_song_repository.get_by_id.assert_called_once_with(1)


def test_positive_get_all(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
):
    song_service = SongService(mocked_song_repository, mocked_upload_file)

    song_service.get_all()

    mocked_song_repository.get_all.assert_called_once()


def test_positive_get_all_with_take_skip(
    mocked_song_repository: SongRepository,
    mocked_upload_file: Callable,
):
    song_service = SongService(mocked_song_repository, mocked_upload_file)

    song_service.get_all(10, 10)

    mocked_song_repository.get_all.assert_called_once_with(10, 10)
