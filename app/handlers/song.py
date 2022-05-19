from flask import Blueprint, request

from app.common.token import token_required
from app.controllers.song import SongController


def create_song_handlers(controller: SongController):
    blueprint = Blueprint("song", __name__)

    # @token_required
    @blueprint.route("/create", methods=["POST"])
    @token_required
    def create(current_user):
        return controller.create(request, current_user)

    @blueprint.route("/update", methods=["POST"])
    @token_required
    def update():
        return controller.update(request)

    @blueprint.route("/delete", methods=["POST"])
    @token_required
    def delete():
        return controller.delete(request)

    @blueprint.route("/get-all", methods=["GET"])
    @token_required
    def get_all():
        return controller.get_all(request)

    @blueprint.route("/get-by-id", methods=["GET"])
    @token_required
    def get_by_id():
        return controller.get_by_id(request)

    return blueprint
