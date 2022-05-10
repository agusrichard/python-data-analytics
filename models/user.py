from datetime import datetime

from models import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(255), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def check_password(self, password: str):
        return check_password_hash(self.password, password)

    @classmethod
    def generate_password(cls, password: str):
        return generate_password_hash(password)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.fullname}')"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "fullname": self.fullname,
            "bio": self.bio,
            "last_login": self.last_login,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        if "password" not in data:
            raise ValueError("Password is required")

        data["password"] = cls.generate_password(data["password"])
        user = cls(**data)

        return user
