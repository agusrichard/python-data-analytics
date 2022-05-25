import pytest
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from app.models.song import Song
from app.models.user import User


NUM_SONGS = 10


@pytest.fixture
def user(db: SQLAlchemy):
    user_ = User(email="test@test.com", username="test")
    user_.set_password("test")

    db.session.add(user_)
    db.session.commit()

    yield user_


@pytest.fixture
def songs(db: SQLAlchemy, user: User):
    for i in range(NUM_SONGS):
        word = f"test-{i}"
        song = Song(
            title=word,
            song_url=word,
            small_thumbnail_url=word,
            large_thumbnail_url=word,
            user_id=user.id,
        )

        db.session.add(song)

    db.session.commit()


def test_positive_create_song_uncommited():
    song = Song(
        title="test",
        song_url="test",
        small_thumbnail_url="test",
        large_thumbnail_url="test",
    )

    assert song.title == "test"
    assert song.song_url == "test"
    assert song.small_thumbnail_url == "test"
    assert song.large_thumbnail_url == "test"


def test_positive_create_song_committed(db: SQLAlchemy, user: User):
    song = Song(
        title="test",
        song_url="test",
        small_thumbnail_url="test",
        large_thumbnail_url="test",
        user_id=user.id,
    )

    db.session.add(song)
    db.session.commit()

    song: Song = Song.query.filter_by(title="test").first()

    assert song.title == "test"
    assert song.song_url == "test"
    assert song.small_thumbnail_url == "test"
    assert song.large_thumbnail_url == "test"
    assert song.user_id == user.id
    assert song.id is not None
    assert song.created_at is not None
    assert song.updated_at is not None


def test_positive_song_repr(db: SQLAlchemy, user: User):
    song = Song(
        title="test",
        song_url="test",
        small_thumbnail_url="test",
        large_thumbnail_url="test",
        user_id=user.id,
    )

    db.session.add(song)
    db.session.commit()

    assert str(song) == f"Song('{song.title}', '{song.song_url}')"


def test_negative_create_song_no_user_id(db: SQLAlchemy):
    with pytest.raises(IntegrityError):
        song = Song(
            title="test",
            song_url="test",
            small_thumbnail_url="test",
            large_thumbnail_url="test",
        )

        db.session.add(song)
        db.session.commit()


def test_negative_create_song_title_not_provided(db: SQLAlchemy, user: User):
    with pytest.raises(IntegrityError):
        song = Song(
            song_url="test",
            small_thumbnail_url="test",
            large_thumbnail_url="test",
            user_id=user.id,
        )

        db.session.add(song)
        db.session.commit()


def test_negative_create_song_song_url_not_provided(db: SQLAlchemy, user: User):
    with pytest.raises(IntegrityError):
        song = Song(
            title="test",
            small_thumbnail_url="test",
            large_thumbnail_url="test",
            user_id=user.id,
        )

        db.session.add(song)
        db.session.commit()


def test_positive_add_song_from_user(db: SQLAlchemy, user: User):
    song = Song(
        title="test",
        song_url="test",
        small_thumbnail_url="test",
        large_thumbnail_url="test",
    )

    user.songs.append(song)

    db.session.add(user)
    db.session.commit()


def test_get_song_by_id(db: SQLAlchemy, user: User):
    song = Song(
        title="test",
        song_url="test",
        small_thumbnail_url="test",
        large_thumbnail_url="test",
        user_id=user.id,
    )

    db.session.add(song)
    db.session.commit()

    song: Song = Song.get_by_id(song.id)

    assert song.title == "test"
    assert song.song_url == "test"
    assert song.small_thumbnail_url == "test"
    assert song.large_thumbnail_url == "test"
    assert song.user_id == user.id


def test_positive_get_songs_directly(user: User, songs: List[Song]):
    list_of_songs = Song.query.filter_by(user_id=user.id).all()

    assert len(list_of_songs) == NUM_SONGS


def test_positive_get_songs_from_user_directly(user: User, songs: List[Song]):
    list_of_songs = user.songs.all()

    assert len(list_of_songs) == NUM_SONGS


def test_positive_get_songs_from_user_with_take_skip(user: User, songs: List[Song]):
    list_of_songs = user.get_songs(take=5, skip=5)

    assert len(list_of_songs) == 5


def test_positive_paginate_songs(user: User, songs: List[Song]):
    list_of_songs = Song.paginate(5, 0)

    assert len(list_of_songs) == 5


def test_positive_update_song(db: SQLAlchemy, user: User):
    song = Song(
        title="test",
        song_url="test",
        small_thumbnail_url="test",
        large_thumbnail_url="test",
        user_id=user.id,
    )

    db.session.add(song)
    db.session.commit()

    song.title = "test_updated"
    song.song_url = "test_updated"
    song.small_thumbnail_url = "test_updated"
    song.large_thumbnail_url = "test_updated"

    db.session.add(song)
    db.session.commit()

    song: Song = Song.query.filter_by(title="test_updated").first()

    assert song.title == "test_updated"
    assert song.song_url == "test_updated"
    assert song.small_thumbnail_url == "test_updated"
    assert song.large_thumbnail_url == "test_updated"


def test_negative_update_song_not_nullable_field_to_none(db: SQLAlchemy, user: User):
    song = Song(
        title="test",
        song_url="test",
        small_thumbnail_url="test",
        large_thumbnail_url="test",
        user_id=user.id,
    )

    db.session.add(song)
    db.session.commit()

    with pytest.raises(IntegrityError):
        song.title = None
        song.song_url = None

        db.session.add(song)
        db.session.commit()


def test_positive_delete_song(db: SQLAlchemy, user: User):
    song = Song(
        title="test",
        song_url="test",
        small_thumbnail_url="test",
        large_thumbnail_url="test",
        user_id=user.id,
    )

    db.session.add(song)
    db.session.commit()

    db.session.delete(song)
    db.session.commit()

    assert Song.query.filter_by(title="test").first() is None


def test_positive_song_from_dict(db: SQLAlchemy, user: User):
    song = Song.from_dict(
        {
            "title": "test",
            "song_url": "test",
            "small_thumbnail_url": "test",
            "large_thumbnail_url": "test",
            "user_id": user.id,
        }
    )

    assert song.title == "test"
    assert song.song_url == "test"
    assert song.small_thumbnail_url == "test"
    assert song.large_thumbnail_url == "test"
    assert song.user_id == user.id


def test_positive_song_to_dict(db: SQLAlchemy, user: User):
    song = Song(
        title="test",
        song_url="test",
        small_thumbnail_url="test",
        large_thumbnail_url="test",
        user_id=user.id,
    )

    db.session.add(song)
    db.session.commit()

    song: Song = Song.query.filter_by(title="test").first()
    song_dict = song.to_dict()

    assert song_dict["title"] == "test"
    assert song_dict["song_url"] == "test"
    assert song_dict["small_thumbnail_url"] == "test"
    assert song_dict["large_thumbnail_url"] == "test"
    assert song_dict["user_id"] == user.id
    assert song_dict["created_at"] is not None
    assert song_dict["updated_at"] is not None
