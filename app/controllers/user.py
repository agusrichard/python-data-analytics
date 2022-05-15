from http import HTTPStatus
from typing import List, Tuple
from flask import Request, Response, jsonify
from app.common.exceptions import BadRequestException

from app.models.user import User
from app.services.user import UserService


class UserController:
    def __init__(self, service: UserService):
        self.service = service

    def follow(self, current_user: User, user_id: int) -> Tuple[Response, int]:
        try:
            self.service.follow(current_user.id, user_id)
        except BadRequestException as e:
            return jsonify(e.to_dict()), e.error_code

    def unfollow(self, current_user: User, user_id: int) -> Tuple[Response, int]:
        try:
            self.service.unfollow(current_user.id, user_id)
        except BadRequestException as e:
            return jsonify(e.to_dict()), e.error_code

    def get_followers(
        self, request: Request, current_user: User
    ) -> Tuple[List[User], int]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        return jsonify(current_user.get_followers(take, skip)), HTTPStatus.OK

    def get_followed_users(
        self, request: Request, current_user: User
    ) -> Tuple[List[User], int]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        return jsonify(current_user.get_followed_users(take, skip)), HTTPStatus.OK
