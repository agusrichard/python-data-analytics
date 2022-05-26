from typing import Optional, List
from flask_sqlalchemy import SQLAlchemy

from app.models.song import Song
from app.models.playlist import Playlist


class PlaylistRepository:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def create(self, data: dict) -> None:
        playlist = Playlist.from_dict(data)
        self.db.session.add(playlist)
        self.db.session.commit()

    def update(self, playlist: Playlist, data: dict) -> None:
        playlist.title = data.get("title", playlist.title)

        self.db.session.commit()

    def delete(self, playlist: Playlist) -> None:
        self.db.session.delete(playlist)
        self.db.session.commit()

    def get_by_id(self, playlist_id: int) -> Optional[Playlist]:
        return Playlist.get_by_id(playlist_id)

    def get_all(self, take: int = 10, skip: int = 0) -> List[Playlist]:
        return Playlist.paginate(take, skip)

    def add_song(self, playlist: Playlist, song: Song) -> None:
        playlist.add_song(song)
        self.db.session.commit()

    def remove_song(self, playlist: Playlist, song: Song) -> None:
        playlist.remove_song(song)
        self.db.session.commit()
