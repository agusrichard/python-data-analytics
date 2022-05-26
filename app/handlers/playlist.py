from flask import Blueprint, request

from app.common.token import token_required
from app.controllers.playlist import PlaylistController


def create_playlist_handler(controller: PlaylistController):
    blueprint = Blueprint("playlist", __name__)

    @blueprint.route("/create", methods=["POST"])
    @token_required
    def create(current_user):
        return controller.create(current_user, request)

    @blueprint.route("/update/<int:playlist_id>", methods=["PUT"])
    @token_required
    def update(current_user, playlist_id):
        return controller.update(current_user, request, playlist_id)

    @blueprint.route("/delete/<int:playlist_id>", methods=["DELETE"])
    @token_required
    def delete(current_user, playlist_id):
        return controller.delete(current_user, playlist_id)

    @blueprint.route("/get-all", methods=["GET"])
    @token_required
    def get_all(_):
        return controller.get_all(request)

    @blueprint.route("/get-by-id/<int:playlist_id>", methods=["GET"])
    @token_required
    def get_by_id(_, playlist_id):
        return controller.get_by_id(request, playlist_id)

    @blueprint.route("/add-song/<int:playlist_id>/<int:song_id>", methods=["POST"])
    @token_required
    def add_song(current_user, playlist_id, song_id):
        return controller.add_song(current_user, playlist_id, song_id)

    @blueprint.route("/remove-song/<int:playlist_id>/<int:song_id>", methods=["POST"])
    @token_required
    def remove_song(current_user, playlist_id, song_id):
        return controller.remove_song(current_user, playlist_id, song_id)

    return blueprint
