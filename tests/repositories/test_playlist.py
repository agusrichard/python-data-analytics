import pytest
from unittest import mock
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from app.models.playlist import Playlist
from app.repositories.playlist import PlaylistRepository


@pytest.fixture
def mocked_db():
    with mock.patch("app.repositories.playlist.SQLAlchemy") as mocked_db_:
        yield mocked_db_


@pytest.fixture
def MockedPlaylist():
    with mock.patch("app.repositories.playlist.Playlist") as MockedPlaylist_:
        yield MockedPlaylist_


def test_positive_create_playlist(mocked_db: SQLAlchemy, MockedPlaylist: Playlist):
    playlist_repository = PlaylistRepository(mocked_db)

    data = {
        "title": "test",
    }

    playlist_repository.create(data)

    mocked_db.session.add.assert_called_once()
    mocked_db.session.commit.assert_called_once()
    MockedPlaylist.from_dict.assert_called_once_with(data)


def test_negative_create_playlist_nullable_fields(
    mocked_db: SQLAlchemy, MockedPlaylist: Playlist
):
    mocked_db.session.commit.side_effect = IntegrityError(
        statement="error", params=None, orig=None
    )

    playlist_repository = PlaylistRepository(mocked_db)

    data = {
        "title": None,
    }

    with pytest.raises(IntegrityError):
        playlist_repository.create(data)

    mocked_db.session.add.assert_called_once()
    mocked_db.session.commit.assert_called_once()
    MockedPlaylist.from_dict.assert_called_once_with(data)


def test_positive_update_playlist(mocked_db: SQLAlchemy, MockedPlaylist: Playlist):
    playlist_repository = PlaylistRepository(mocked_db)

    data = {
        "title": "test",
    }

    playlist_repository.update(MockedPlaylist.return_value, data)

    mocked_db.session.commit.assert_called_once()


def test_positive_update_playlist_required_to_none(
    mocked_db: SQLAlchemy, MockedPlaylist: Playlist
):
    mocked_db.session.commit.side_effect = IntegrityError(
        statement="error", params=None, orig=None
    )
    playlist_repository = PlaylistRepository(mocked_db)

    data = {
        "title": None,
    }

    with pytest.raises(IntegrityError):
        playlist_repository.update(MockedPlaylist.return_value, data)

    mocked_db.session.commit.assert_called_once()


def test_positive_delete_playlist(mocked_db: SQLAlchemy, MockedPlaylist: Playlist):
    playlist_repository = PlaylistRepository(mocked_db)

    playlist_repository.delete(MockedPlaylist.return_value)

    mocked_db.session.delete.assert_called_once()
    mocked_db.session.commit.assert_called_once()


def test_positive_playlist_get_by_id(mocked_db: SQLAlchemy, MockedPlaylist: Playlist):
    playlist_repository = PlaylistRepository(mocked_db)

    playlist_repository.get_by_id(1)

    MockedPlaylist.get_by_id.assert_called_once_with(1)


def test_positive_playlist_get_all(mocked_db: SQLAlchemy, MockedPlaylist: Playlist):
    playlist_repository = PlaylistRepository(mocked_db)

    playlist_repository.get_all()

    MockedPlaylist.paginate.assert_called_once()


def test_positive_playlist_get_all_with_takeskip(
    mocked_db: SQLAlchemy, MockedPlaylist: Playlist
):
    playlist_repository = PlaylistRepository(mocked_db)

    playlist_repository.get_all(5, 5)

    MockedPlaylist.paginate.assert_called_once_with(5, 5)


def test_positive_add_song_to_playlist(mocked_db: SQLAlchemy, MockedPlaylist: Playlist):
    song = mock.MagicMock()
    playlist = MockedPlaylist()

    playlist_repository = PlaylistRepository(mocked_db)

    playlist_repository.add_song(playlist, song)

    playlist.add_song.assert_called_once()
    mocked_db.session.commit.assert_called_once()


def test_positive_remove_song_from_playlist(
    mocked_db: SQLAlchemy, MockedPlaylist: Playlist
):
    song = mock.MagicMock()
    playlist = MockedPlaylist()

    playlist_repository = PlaylistRepository(mocked_db)

    playlist_repository.remove_song(playlist, song)

    playlist.remove_song.assert_called_once()
    mocked_db.session.commit.assert_called_once()
