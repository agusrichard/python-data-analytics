from datetime import datetime
from typing import List, Optional

from app import db
from app.models.song import Song

playlist_songs = db.Table(
    "playlist_songs",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id")),
    db.Column("song_id", db.Integer, db.ForeignKey("songs.id")),
)


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    songs = db.relationship(
        "Song",
        secondary="playlist_songs",
        lazy="dynamic",
        backref=db.backref("playlists", lazy="dynamic"),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def paginate(cls, take: int = 10, skip: int = 0) -> List["Playlist"]:
        return cls.query.offset(skip).limit(take).all()

    def __repr__(self) -> str:
        return f"Playlist('{self.title}')"

    @classmethod
    def get_by_id(cls, playlist_id: int) -> Optional["Playlist"]:
        return cls.query.filter_by(id=playlist_id).first()

    @classmethod
    def from_dict(cls, data: dict) -> "Playlist":
        return cls(**data)

    def add_song(self, song: Song):
        self.songs.append(song)

    def remove_song(self, song: Song):
        self.songs.remove(song)

    def get_songs(self, take: int = 10, skip: int = 0) -> List["Song"]:
        return self.songs.offset(skip).limit(take).all()
