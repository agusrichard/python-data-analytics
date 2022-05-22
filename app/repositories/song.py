from typing import Optional, List
from flask_sqlalchemy import SQLAlchemy

from app.models.song import Song


class SongRepository:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def create(self, data: dict) -> None:
        song = Song.from_dict(data)
        self.db.session.add(song)
        self.db.session.commit()

    def update(self, id: int, data: dict) -> None:
        song = self.get_by_id(id)
        if not song:
            return None

        print("update repository song", data)

        song.title = data.get("title", song.title)
        song.song_url = data.get("song_url", song.song_url)
        song.small_thumbnail_url = data.get(
            "small_thumbnail_url", song.small_thumbnail_url
        )
        song.large_thumbnail_url = data.get(
            "large_thumbnail_url", song.large_thumbnail_url
        )

        print("song_dict", song.to_dict())

        self.db.session.commit()

    def delete(self, id: int) -> None:
        song = self.get_by_id(id)
        if not song:
            return None

        self.db.session.delete(song)
        self.db.session.commit()

    def get_by_id(self, id: int) -> Optional[Song]:
        return Song.query.get(id)

    def get_all(self, take: int = 10, skip: int = 0) -> List[Song]:
        return Song.paginate(take, skip)
