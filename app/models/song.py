from datetime import datetime
from sqlalchemy.orm import relationship

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
