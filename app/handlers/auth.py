from flask import Blueprint, request

from app.common.token import token_required
from app.controllers.auth import AuthController


def create_auth_handlers(controller: AuthController):
    blueprint = Blueprint("auth", __name__)

    @blueprint.route("/login", methods=["POST"])
    def login():
        return controller.login(request)

    @blueprint.route("/register", methods=["POST"])
    def register():
        return controller.register(request)

    @blueprint.route("/profile", methods=["GET"])
    @token_required
    def profile(current_user):
        return controller.profile(current_user)

    return blueprint
