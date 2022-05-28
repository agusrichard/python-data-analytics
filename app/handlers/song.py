from flask import Blueprint, request

from app.common.token import token_required
from app.controllers.song import SongController


class SongHandler:
    def __init__(self, controller: SongController) -> None:
        self.__blueprint = Blueprint("song", __name__)
        self.__blueprint.add_url_rule(
            "/create",
            "create",
            token_required(controller.create),
            methods=["POST"],
        )
        self.__blueprint.add_url_rule(
            "/update/<int:song_id>",
            "update",
            token_required(controller.update),
            methods=["PUT"],
        )
        self.__blueprint.add_url_rule(
            "/delete/<int:song_id>",
            "delete",
            token_required(controller.delete),
            methods=["DELETE"],
        )
        self.__blueprint.add_url_rule(
            "/get-all", "get_all", token_required(controller.get_all), methods=["GET"]
        )
        self.__blueprint.add_url_rule(
            "/get-by-id/<int:song_id>",
            "get_by_id",
            token_required(controller.get_by_id),
            methods=["GET"],
        )

    @property
    def blueprint(self) -> Blueprint:
        return self.__blueprint
