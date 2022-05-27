import pytest
from typing import List, Tuple
from flask_sqlalchemy import SQLAlchemy

from app.models.user import User
from app.models.song import Song
from app.models.playlist import Playlist

PLAYLIST1_NAME = "Playlist 1"


@pytest.fixture
def user(db: SQLAlchemy):
    user_ = User(email="test@test.com", username="test")
    user_.set_password("test")

    db.session.add(user_)
    db.session.commit()

    yield user_


@pytest.fixture
def initialize(db: SQLAlchemy, user: User):
    playlist = Playlist(title=PLAYLIST1_NAME, user_id=user.id)

    db.session.add(playlist)
    db.session.commit()

    yield db, user, playlist


@pytest.fixture
def playlist_with_songs(initialize: Tuple[SQLAlchemy, User, Playlist]):
    db, user, playlist = initialize

    songs = []
    for _ in range(10):
        song = Song(
            title="test",
            song_url="test",
            small_thumbnail_url="test",
            large_thumbnail_url="test",
            user_id=user.id,
        )
        db.session.add(song)
        songs.append(song)

    db.session.commit()

    for song in songs:
        playlist.add_song(song)

    db.session.commit()

    yield playlist, songs


def test_positive_create_playlist_uncommited(
    initialize: Tuple[SQLAlchemy, User, Playlist]
):
    db, user, _ = initialize
    playlist = Playlist(title=PLAYLIST1_NAME, user_id=user.id)
    assert playlist.title == PLAYLIST1_NAME
    assert playlist.created_at is None
    assert playlist.updated_at is None


def test_positive_create_playlist_committed(
    initialize: Tuple[SQLAlchemy, User, Playlist]
):
    db, user, _ = initialize
    playlist = Playlist(title=PLAYLIST1_NAME, user_id=user.id)

    db.session.add(playlist)
    db.session.commit()

    playlist = Playlist.query.filter_by(title=PLAYLIST1_NAME).first()

    assert playlist.id is not None
    assert playlist.title == PLAYLIST1_NAME
    assert playlist.created_at is not None
    assert playlist.updated_at is not None


def test_positive_playlist_to_dict(initialize: Tuple[SQLAlchemy, User, Playlist]):
    _, _, playlist = initialize
    playlist_dict = playlist.to_dict()

    assert playlist_dict["id"] == playlist.id
    assert playlist_dict["title"] == playlist.title
    assert playlist_dict["created_at"] == playlist.created_at.isoformat()
    assert playlist_dict["updated_at"] == playlist.updated_at.isoformat()
    assert playlist_dict["user_id"] == playlist.user_id


def test_positive_playlist_repr(initialize: Tuple[SQLAlchemy, User, Playlist]):
    _, _, playlist = initialize

    assert str(playlist) == f"Playlist('{playlist.title}')"


def test_positive_get_playlist_by_id(initialize: Tuple[SQLAlchemy, User, Playlist]):
    playlist = Playlist.get_by_id(1)

    assert playlist.id is not None
    assert playlist.title == PLAYLIST1_NAME
    assert playlist.created_at is not None
    assert playlist.updated_at is not None


def test_positive_create_playlist_from_dict(db: SQLAlchemy, user: User):
    playlist = Playlist.from_dict({"title": PLAYLIST1_NAME, "user_id": user.id})

    db.session.add(playlist)
    db.session.commit()

    assert playlist.id is not None
    assert playlist.title == PLAYLIST1_NAME
    assert playlist.created_at is not None
    assert playlist.updated_at is not None


def test_positive_playlist_paginate(db: SQLAlchemy, user: User):
    for _ in range(10):
        playlist = Playlist(title=PLAYLIST1_NAME, user_id=user.id)
        db.session.add(playlist)

    db.session.commit()

    playlists = Playlist.paginate(10, 0)

    assert len(playlists) == 10


def test_positive_add_songs_to_playlist(
    playlist_with_songs: Tuple[Playlist, List[Song]]
):
    playlist, songs = playlist_with_songs

    assert playlist is not None
    assert songs is not None

    songs_from_playlist = playlist.get_songs()
    assert len(songs_from_playlist) == len(songs)
    for i in range(len(songs)):
        assert songs[i].id == songs_from_playlist[i].id


def test_positive_remove_songs_from_playlist(
    playlist_with_songs: Tuple[Playlist, List[Song]]
):
    playlist, songs = playlist_with_songs

    for song in songs:
        playlist.remove_song(song)

    assert len(playlist.get_songs()) == 0
