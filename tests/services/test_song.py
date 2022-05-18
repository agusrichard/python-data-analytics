import pytest
from unittest import mock

from app.services.song import SongService
from app.repositories.song import SongRepository


@pytest.fixture
def mocked_song_repository():
    with mock.patch("app.services.song.SongRepository") as MockedSongRepository:
        yield MockedSongRepository.return_value


def test_positive_create_song(mocked_song_repository: SongRepository):
    mocked_song_repository.create.return_value = mock.MagicMock()

    song_service = SongService(mocked_song_repository)

    data = {
        "title": "test",
        "song_url": "test",
        "small_thumbnail_url": "test",
        "large_thumbnail_url": "test",
    }

    song_service.create(data)

    mocked_song_repository.create.assert_called_once_with(data)


def test_positive_update_song(mocked_song_repository: SongRepository):
    mocked_song_repository.update.return_value = mock.MagicMock()

    song_service = SongService(mocked_song_repository)

    data = {
        "title": "test",
        "song_url": "test",
        "small_thumbnail_url": "test",
        "large_thumbnail_url": "test",
    }

    song_service.update(1, data)

    mocked_song_repository.update.assert_called_once_with(1, data)


def test_positive_delete(mocked_song_repository: SongRepository):
    mocked_song_repository.delete.return_value = mock.MagicMock()

    song_service = SongService(mocked_song_repository)

    song_service.delete(1)

    mocked_song_repository.delete.assert_called_once_with(1)


def test_positive_get_by_id(mocked_song_repository: SongRepository):
    mocked_song_repository.get_by_id.return_value = mock.MagicMock()

    song_service = SongService(mocked_song_repository)

    song_service.get_by_id(1)

    mocked_song_repository.get_by_id.assert_called_once_with(1)


def test_positive_get_all(mocked_song_repository: SongRepository):
    mocked_song_repository.get_all.return_value = mock.MagicMock()

    song_service = SongService(mocked_song_repository)

    song_service.get_all()

    mocked_song_repository.get_all.assert_called_once()
