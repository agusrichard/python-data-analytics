from typing import Tuple
from http import HTTPStatus
from flask import Request, Response, jsonify
from app.common.messages import USER_ID_REQUIRED
from app.common.exceptions import NotFoundException

from app.models.user import User
from app.services.user import UserService


class UserController:
    def __init__(self, service: UserService):
        self.service = service

    def follow(self, request: Request, current_user: User) -> Tuple[Response, int]:
        try:
            user_id = request.args.get("user_id", None, int)
            if user_id is None:
                return jsonify({"message": USER_ID_REQUIRED}), HTTPStatus.BAD_REQUEST

            self.service.follow(current_user, user_id)

            return "", HTTPStatus.OK
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code

    def unfollow(self, request: Request, current_user: User) -> Tuple[Response, int]:
        try:
            user_id = request.args.get("user_id", None, int)
            if user_id is None:
                return jsonify({"message": USER_ID_REQUIRED}), HTTPStatus.BAD_REQUEST

            self.service.unfollow(current_user, user_id)

            return "", HTTPStatus.OK
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code

    def get_followers(
        self, request: Request, current_user: User
    ) -> Tuple[Response, int]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        users = current_user.get_followers(take, skip)
        return (
            jsonify({"followers": [user.to_dict() for user in users]}),
            HTTPStatus.OK,
        )

    def get_followed_users(
        self, request: Request, current_user: User
    ) -> Tuple[Response, int]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        users = current_user.get_followed_users(take, skip)
        return (
            jsonify({"followed_users": [user.to_dict() for user in users]}),
            HTTPStatus.OK,
        )
