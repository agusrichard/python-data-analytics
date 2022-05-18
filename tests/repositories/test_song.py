import pytest
from unittest import mock
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from app.models.song import Song
from app.repositories.song import SongRepository


@pytest.fixture
def mocked_db():
    with mock.patch("app.repositories.song.SQLAlchemy") as mocked_db_:
        yield mocked_db_


@pytest.fixture
def MockedSong():
    with mock.patch("app.repositories.song.Song") as MockedSong_:
        yield MockedSong_


def test_positive_create_song(mocked_db: SQLAlchemy, MockedSong: Song):
    song_repository = SongRepository(mocked_db)

    data = {
        "title": "test",
        "song_url": "test",
        "small_thumbnail_url": "test",
        "large_thumbnail_url": "test",
    }

    song_repository.create(data)

    mocked_db.session.add.assert_called_once()
    mocked_db.session.commit.assert_called_once()
    MockedSong.from_dict.assert_called_once_with(data)


def test_negative_create_song_nullable_fields(mocked_db: SQLAlchemy, MockedSong: Song):
    mocked_db.session.commit.side_effect = IntegrityError(
        statement="error", params=None, orig=None
    )

    song_repository = SongRepository(mocked_db)

    data = {
        "title": None,
        "song_url": None,
    }

    with pytest.raises(IntegrityError):
        song_repository.create(data)

    mocked_db.session.add.assert_called_once()
    mocked_db.session.commit.assert_called_once()
    MockedSong.from_dict.assert_called_once_with(data)


def test_positive_get_song_by_id(mocked_db: SQLAlchemy, MockedSong: Song):
    song_repository = SongRepository(mocked_db)

    song_repository.get_by_id(1)

    MockedSong.get_by_id.assert_called_once_with(1)


def test_positive_update_song(mocked_db: SQLAlchemy, MockedSong: Song):
    song_repository = SongRepository(mocked_db)

    data = {
        "title": "test",
        "song_url": "test",
        "small_thumbnail_url": "test",
        "large_thumbnail_url": "test",
    }

    song_repository.update(1, data)

    mocked_db.session.commit.assert_called_once()
    MockedSong.get_by_id.assert_called_once_with(1)


def test_negative_update_song_not_found(mocked_db: SQLAlchemy, MockedSong: Song):
    MockedSong.get_by_id.return_value = None

    song_repository = SongRepository(mocked_db)

    data = {
        "title": "test",
        "song_url": "test",
        "small_thumbnail_url": "test",
        "large_thumbnail_url": "test",
    }

    song_repository.update(1, data)

    mocked_db.session.commit.assert_not_called()


def test_negative_update_song_required_to_none(mocked_db: SQLAlchemy, MockedSong: Song):
    mocked_db.session.commit.side_effect = IntegrityError(
        statement="error", params=None, orig=None
    )

    song_repository = SongRepository(mocked_db)

    data = {
        "title": None,
        "song_url": None,
        "small_thumbnail_url": "test",
        "large_thumbnail_url": "test",
    }

    with pytest.raises(IntegrityError):
        song_repository.update(1, data)


def test_positive_delete_song(mocked_db: SQLAlchemy, MockedSong: Song):
    song_repository = SongRepository(mocked_db)

    song_repository.delete(1)

    mocked_db.session.delete.assert_called_once()
    mocked_db.session.commit.assert_called_once()
    MockedSong.get_by_id.assert_called_once_with(1)


def test_negative_delete_song_not_found(mocked_db: SQLAlchemy, MockedSong: Song):
    MockedSong.get_by_id.return_value = None

    song_repository = SongRepository(mocked_db)

    song_repository.delete(1)

    mocked_db.session.delete.assert_not_called()
    mocked_db.session.commit.assert_not_called()
    MockedSong.get_by_id.assert_called_once_with(1)


def test_positive_get_all_songs_default(mocked_db: SQLAlchemy, MockedSong: Song):
    song_repository = SongRepository(mocked_db)

    song_repository.get_all()

    MockedSong.paginate.assert_called_once()


def test_positive_get_all_songs_with_take_skip(mocked_db: SQLAlchemy, MockedSong: Song):
    song_repository = SongRepository(mocked_db)

    song_repository.get_all(take=5, skip=1)

    MockedSong.paginate.assert_called_once_with(5, 1)
