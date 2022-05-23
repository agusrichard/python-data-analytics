from flask import Blueprint, request

from app.common.token import token_required
from app.controllers.song import SongController


def create_song_handlers(controller: SongController):
    blueprint = Blueprint("song", __name__)

    @blueprint.route("/create", methods=["POST"])
    @token_required
    def create(current_user):
        print("create song files", request.files)
        return controller.create(request, current_user)

    @blueprint.route("/update/<int:song_id>", methods=["PUT"])
    @token_required
    def update(current_user, song_id):
        return controller.update(current_user, song_id, request)

    @blueprint.route("/delete/<int:song_id>", methods=["DELETE"])
    @token_required
    def delete(current_user, song_id):
        return controller.delete(current_user, song_id)

    @blueprint.route("/get-all", methods=["GET"])
    @token_required
    def get_all():
        return controller.get_all(request)

    @blueprint.route("/get-by-id/<int:song_id>", methods=["GET"])
    @token_required
    def get_by_id(_, song_id):
        return controller.get_by_id(song_id)

    return blueprint
