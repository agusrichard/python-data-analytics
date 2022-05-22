from datetime import datetime
from typing import List, Optional

from app import db


class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    song_url = db.Column(db.Text, nullable=False)
    small_thumbnail_url = db.Column(db.Text, nullable=True)
    large_thumbnail_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "song_url": self.song_url,
            "small_thumbnail_url": self.small_thumbnail_url,
            "large_thumbnail_url": self.large_thumbnail_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_id": self.user_id,
        }

    @classmethod
    def paginate(cls, take: int = 10, skip: int = 0) -> List["Song"]:
        return cls.query.offset(skip).limit(take).all()

    def __repr__(self) -> str:
        return f"Song('{self.title}', '{self.song_url}')"

    @classmethod
    def get_by_id(cls, id: int) -> Optional["Song"]:
        return cls.query.filter_by(id=id).first()

    @classmethod
    def from_dict(cls, data: dict) -> "Song":
        return cls(**data)
