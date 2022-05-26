import pytest
from unittest import mock

from app.models.user import User
from app.repositories.song import SongRepository
from app.services.playlist import PlaylistService
from app.repositories.playlist import PlaylistRepository
from app.common.exceptions import (
    FieldRequiredException,
    NotFoundException,
    UnauthorizedException,
)


@pytest.fixture
def mocked_playlist_repository():
    with mock.patch(
        "app.services.playlist.PlaylistRepository"
    ) as MockedPlaylistRepository:
        yield MockedPlaylistRepository.return_value


@pytest.fixture
def mocked_song_repository():
    with mock.patch("app.services.playlist.SongRepository") as MockedSongRepository:
        yield MockedSongRepository.return_value


@pytest.fixture
def mocked_current_user():
    yield mock.MagicMock()


def test_positive_create_playlist(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
):
    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    playlist_service.create({"title": "test"})

    mocked_playlist_repository.create.assert_called_once_with({"title": "test"})


def test_negative_create_playlist_required_field(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
):
    data = {}

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(FieldRequiredException):
        playlist_service.create(data)

    mocked_playlist_repository.create.assert_not_called()


def test_positive_update_playlist(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    playlist_service.update(mocked_current_user, 1, {"title": "test"})

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.update.assert_called_once()


def test_negative_update_playlist_not_found(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist_repository.get_by_id.return_value = None
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(NotFoundException):
        playlist_service.update(mocked_current_user, 1, {"title": "test"})

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.update.assert_not_called()


def test_negative_update_playlist_unauthorized(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_current_user.id = 2

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(UnauthorizedException):
        playlist_service.update(mocked_current_user, 1, {"title": "test"})

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.update.assert_not_called()


def test_positive_delete_playlist(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    playlist_service.delete(mocked_current_user, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.delete.assert_called_once()


def test_negative_delete_playlist_not_found(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist_repository.get_by_id.return_value = None
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(NotFoundException):
        playlist_service.delete(mocked_current_user, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.delete.assert_not_called()


def test_negative_delete_playlist_unauthorized(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_current_user.id = 2

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(UnauthorizedException):
        playlist_service.delete(mocked_current_user, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.delete.assert_not_called()


def test_positive_playlist_get_by_id(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    playlist_service.get_by_id(1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist.to_dict.assert_called_once()


def test_negative_playlist_get_by_id_not_found(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
):
    mocked_playlist_repository.get_by_id.return_value = None

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(NotFoundException):
        playlist_service.get_by_id(1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)


def test_positive_playlist_get_all_default(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist_repository.get_all.return_value = [mocked_playlist]

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    playlist_service.get_all()

    mocked_playlist_repository.get_all.assert_called_once()
    mocked_playlist.to_dict.assert_called_once()


def test_positive_playlist_get_all_with_take_skip(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist_repository.get_all.return_value = [mocked_playlist]

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    playlist_service.get_all(take=1, skip=1)

    mocked_playlist_repository.get_all.assert_called_once_with(1, 1)
    mocked_playlist.to_dict.assert_called_once()


def test_positive_playlist_add_song(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_song = mock.MagicMock()
    mocked_song_repository.get_by_id.return_value = mocked_song
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    playlist_service.add_song(mocked_current_user, 1, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.add_song.assert_called_once()


def test_negative_playlist_add_song_playlist_not_found(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist_repository.get_by_id.return_value = None
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(NotFoundException):
        playlist_service.add_song(mocked_current_user, 1, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.get_by_id.assert_not_called()
    mocked_playlist_repository.add_song.assert_not_called()


def test_negative_playlist_add_song_song_not_found(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_song_repository.get_by_id.return_value = None
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(NotFoundException):
        playlist_service.add_song(mocked_current_user, 1, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.add_song.assert_not_called()


def test_negative_playlist_add_song_unauthorized(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_song = mock.MagicMock()
    mocked_song_repository.get_by_id.return_value = mocked_song
    mocked_current_user.id = 2

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(UnauthorizedException):
        playlist_service.add_song(mocked_current_user, 1, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.get_by_id.assert_not_called()
    mocked_playlist_repository.add_song.assert_not_called()


def test_positive_playlist_remove_song(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_song = mock.MagicMock()
    mocked_song_repository.get_by_id.return_value = mocked_song
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    playlist_service.remove_song(mocked_current_user, 1, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.remove_song.assert_called_once()


def test_negative_playlist_remove_song_playlist_not_found(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist_repository.get_by_id.return_value = None
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(NotFoundException):
        playlist_service.remove_song(mocked_current_user, 1, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.get_by_id.assert_not_called()
    mocked_playlist_repository.remove_song.assert_not_called()


def test_negative_playlist_remove_song_song_not_found(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_song_repository.get_by_id.return_value = None
    mocked_current_user.id = 1

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(NotFoundException):
        playlist_service.remove_song(mocked_current_user, 1, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.get_by_id.assert_called_once_with(1)
    mocked_playlist_repository.remove_song.assert_not_called()


def test_negative_playlist_remove_song_unauthorized(
    mocked_playlist_repository: PlaylistRepository,
    mocked_song_repository: SongRepository,
    mocked_current_user,
):
    mocked_playlist = mock.MagicMock()
    mocked_playlist.user_id = 1
    mocked_playlist_repository.get_by_id.return_value = mocked_playlist
    mocked_song = mock.MagicMock()
    mocked_song_repository.get_by_id.return_value = mocked_song
    mocked_current_user.id = 2

    playlist_service = PlaylistService(
        mocked_playlist_repository, mocked_song_repository
    )
    with pytest.raises(UnauthorizedException):
        playlist_service.remove_song(mocked_current_user, 1, 1)

    mocked_playlist_repository.get_by_id.assert_called_once_with(1)
    mocked_song_repository.get_by_id.assert_not_called()
    mocked_playlist_repository.remove_song.assert_not_called()
