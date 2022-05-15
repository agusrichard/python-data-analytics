import jwt
from typing import List
from flask import current_app
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("users.id")),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    fullname = db.Column(db.String(255), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    followed = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    def check_password(self, password: str):
        return check_password_hash(self._password, password)

    def set_password(self, password: str):
        self._password = generate_password_hash(password)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "fullname": self.fullname,
            "bio": self.bio,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "avatar": self.avatar,
            "last_login": None
            if self.last_login is None
            else self.last_login.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        if "password" not in data:
            raise ValueError("Password is required")

        password = data.pop("password")
        user = cls(**data)
        user.set_password(password)

        return user

    def generate_token(self) -> str:
        token = jwt.encode(
            {"id": self.id, "exp": datetime.utcnow() + timedelta(days=1)},
            current_app.config["SECRET_KEY"],
            "HS256",
        )
        return token.decode("utf-8")

    def is_following(self, user: "User") -> bool:
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user: "User") -> None:
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user: "User") -> None:
        if self.is_following(user):
            self.followed.remove(user)

    def get_followers(self, take: int = 10, skip: int = 0) -> List["User"]:
        result = self.followers.limit(take).offset(skip).all()
        return [user.to_dict() for user in result]

    def get_followed_users(self, take: int = 10, skip: int = 0) -> List["User"]:
        result = self.followed.limit(take).offset(skip).all()
        return [user.to_dict() for user in result]

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, _):
        raise ValueError("Can't set plain password, use set_password instead")
