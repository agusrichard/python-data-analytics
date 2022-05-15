from flask import Blueprint, request

from app.common.token import token_required
from app.controllers.user import UserController


def create_user_handlers(controller: UserController):
    blueprint = Blueprint("user", __name__)

    @blueprint.route("/follow", methods=["POST"])
    @token_required
    def follow(current_user):
        return controller.follow(request, current_user)

    @blueprint.route("/unfollow", methods=["POST"])
    @token_required
    def unfollow(current_user):
        return controller.unfollow(request, current_user)

    @blueprint.route("/get-followers", methods=["GET"])
    @token_required
    def get_followers(current_user):
        return controller.get_followers(request, current_user)

    @blueprint.route("/get-followed-users", methods=["GET"])
    @token_required
    def get_followed_users(current_user):
        return controller.get_followed_users(request, current_user)

    return blueprint
