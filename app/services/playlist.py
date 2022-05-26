from typing import List, Dict

from app.models.user import User
from app.repositories.song import SongRepository
from app.repositories.playlist import PlaylistRepository
from app.common.exceptions import (
    FieldRequiredException,
    NotFoundException,
    UnauthorizedException,
)
from app.common.messages import (
    SONG_NOT_FOUND,
    PLAYLIST_NOT_FOUND,
    UNAUTHORIZED_TO_DELETE_PLAYLIST,
    UNAUTHORIZED_TO_UPDATE_PLAYLIST,
    UNAUTHORIZED_ADD_SONG_TO_PLAYLIST,
    UNAUTHORIZED_REMOVE_SONG_FROM_PLAYLIST,
)


class PlaylistService:
    def __init__(
        self, playlist_repository: PlaylistRepository, song_repository: SongRepository
    ) -> None:
        self.playlist_repository = playlist_repository
        self.song_repository = song_repository

    def create(self, data: Dict[str, str]) -> None:
        if "title" not in data or not data["title"]:
            raise FieldRequiredException("title")

        self.playlist_repository.create(data)

    def update(self, current_user: User, playlist_id: int, data: dict) -> None:
        playlist = self.playlist_repository.get_by_id(playlist_id)
        if playlist is None:
            raise NotFoundException(PLAYLIST_NOT_FOUND)

        if current_user.id != playlist.user_id:
            raise UnauthorizedException(UNAUTHORIZED_TO_UPDATE_PLAYLIST)

        self.playlist_repository.update(playlist, data)

    def delete(self, current_user: User, playlist_id: int) -> None:
        playlist = self.playlist_repository.get_by_id(playlist_id)
        if playlist is None:
            raise NotFoundException(PLAYLIST_NOT_FOUND)

        if current_user.id != playlist.user_id:
            raise UnauthorizedException(UNAUTHORIZED_TO_DELETE_PLAYLIST)

        self.playlist_repository.delete(playlist)

    def get_by_id(
        self, playlist_id: int, take_songs: int = 10, skip_songs: int = 0
    ) -> dict:
        playlist = self.playlist_repository.get_by_id(playlist_id)
        if playlist is None:
            raise NotFoundException(PLAYLIST_NOT_FOUND)

        playlist_dict = playlist.to_dict()
        songs = playlist.get_songs(take_songs, skip_songs)
        playlist_dict["songs"] = [song.to_dict() for song in songs]
        return playlist_dict

    def get_all(self, take: int = 10, skip: int = 0) -> List[dict]:
        playlists = self.playlist_repository.get_all(take, skip)
        return [playlist.to_dict() for playlist in playlists]

    def add_song(self, current_user: User, playlist_id: int, song_id: int) -> None:
        playlist = self.playlist_repository.get_by_id(playlist_id)
        if playlist is None:
            raise NotFoundException(PLAYLIST_NOT_FOUND)

        if playlist.user_id != current_user.id:
            raise UnauthorizedException(UNAUTHORIZED_ADD_SONG_TO_PLAYLIST)

        song = self.song_repository.get_by_id(song_id)
        if song is None:
            raise NotFoundException(SONG_NOT_FOUND)

        self.playlist_repository.add_song(playlist, song)

    def remove_song(self, current_user: User, playlist_id: int, song_id: int) -> None:
        playlist = self.playlist_repository.get_by_id(playlist_id)
        if playlist is None:
            raise NotFoundException(PLAYLIST_NOT_FOUND)

        if playlist.user_id != current_user.id:
            raise UnauthorizedException(UNAUTHORIZED_REMOVE_SONG_FROM_PLAYLIST)

        song = self.song_repository.get_by_id(song_id)
        if song is None:
            raise NotFoundException(SONG_NOT_FOUND)

        self.playlist_repository.remove_song(playlist, song)
