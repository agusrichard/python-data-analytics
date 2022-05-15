from typing import List
from flask import Request

from app.models.user import User
from app.services.user import UserService


class UserController:
    def __init__(self, service: UserService):
        self.service = service

    def follow(self, current_user, user_id) -> None:
        self.service.follow(current_user.id, user_id)

    def unfollow(self, current_user: User, user_id) -> None:
        self.service.unfollow(current_user.id, user_id)

    def get_followers(self, request: Request, current_user: User) -> List[User]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        return current_user.get_followers(take, skip)

    def get_followed_users(self, request: Request, current_user: User) -> List[User]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        return current_user.get_followed_users(take, skip)
