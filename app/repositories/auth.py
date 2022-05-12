from typing import List
from flask_sqlalchemy import SQLAlchemy

from app.models.user import User


class AuthRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, data) -> None:
        user = User.from_dict(data)
        self.db.session.add(user)
        self.db.session.commit()

    def update(self, id, data) -> None:
        user = self.get_by_id(id)
        if not user:
            return None

        user.fullname = data["fullname"]
        user.bio = data["bio"]
        user.last_login = data["last_login"]

        self.db.session.commit()

    def get_all(self, limit: int = 10, offset: int = 0) -> List[User]:
        return User.query.limit(limit).offset(offset).all()

    def get_by_id(self, id: int) -> User:
        return User.query.get(id)

    def get_by_email(self, email: str) -> User:
        return User.query.filter_by(email=email).first()
