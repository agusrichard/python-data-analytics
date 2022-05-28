from flask import Blueprint, request

from app.common.token import token_required
from app.controllers.user import UserController


class UserHandler:
    def __init__(self, controller: UserController) -> None:
        self.__blueprint = Blueprint("user", __name__)
        self.__blueprint.add_url_rule(
            "/follow", "follow", token_required(controller.follow), methods=["POST"]
        )
        self.__blueprint.add_url_rule(
            "/unfollow",
            "unfollow",
            token_required(controller.unfollow),
            methods=["POST"],
        )
        self.__blueprint.add_url_rule(
            "/get-followers",
            "get_followers",
            token_required(controller.get_followers),
            methods=["GET"],
        )
        self.__blueprint.add_url_rule(
            "/get-followed-users",
            "get_followed_users",
            token_required(controller.get_followed_users),
            methods=["GET"],
        )
        self.__blueprint.add_url_rule(
            "/get-songs-by-user-id/<int:user_id>",
            "get_songs",
            token_required(controller.get_songs),
            methods=["GET"],
        )

    @property
    def blueprint(self) -> Blueprint:
        return self.__blueprint
