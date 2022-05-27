from flask import Blueprint

from app.common.token import token_required
from app.controllers.playlist import PlaylistController


class PlaylistHandler:
    def __init__(self, controller: PlaylistController):
        self.__blueprint = Blueprint("playlist", __name__)
        self.__blueprint.add_url_rule(
            "/create", "create", token_required(controller.create), methods=["POST"]
        )
        self.__blueprint.add_url_rule(
            "/update/<int:playlist_id>",
            "update",
            token_required(controller.update),
            methods=["PUT"],
        )
        self.__blueprint.add_url_rule(
            "/delete/<int:playlist_id>",
            "delete",
            token_required(controller.delete),
            methods=["DELETE"],
        )
        self.__blueprint.add_url_rule(
            "/get-all", "get_all", token_required(controller.get_all), methods=["GET"]
        )
        self.__blueprint.add_url_rule(
            "/get-by-id/<int:playlist_id>",
            "get_by_id",
            token_required(controller.get_by_id),
            methods=["GET"],
        )
        self.__blueprint.add_url_rule(
            "/add-song/<int:playlist_id>/<int:song_id>",
            "add_song",
            token_required(controller.add_song),
            methods=["POST"],
        )
        self.__blueprint.add_url_rule(
            "/remove-song/<int:playlist_id>/<int:song_id>",
            "remove_song",
            token_required(controller.remove_song),
            methods=["POST"],
        )

    @property
    def blueprint(self):
        return self.__blueprint
