from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy

from app.models.user import User


class UserRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, data) -> None:
        user = User.from_dict(data)
        self.db.session.add(user)
        self.db.session.commit()

    def update(self, user_id, data) -> None:
        user = self.get_by_id(user_id)
        if not user:
            return None

        user.fullname = data.get("fullname", user.fullname)
        user.bio = data.get("bio", user.bio)
        user.last_login = data.get("last_login", user.last_login)
        user.avatar = data.get("avatar", user.avatar)

        self.db.session.commit()

        return None

    def get_all(self, take: int = 10, skip: int = 0) -> List[User]:
        return User.query.limit(take).offset(skip).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    def follow(self, from_user: User, to_user: User) -> None:
        from_user.follow(to_user)
        self.db.session.commit()

    def unfollow(self, from_user: User, to_user: User) -> None:
        from_user.unfollow(to_user)
        self.db.session.commit()
