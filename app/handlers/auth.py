from flask import Blueprint, request

from app.common.token import token_required
from app.controllers.auth import AuthController


def create_auth_handlers(controller: AuthController):
    blueprint = Blueprint("auth", __name__)

    @blueprint.route("/login", methods=["POST"])
    def login():
        data = request.json
        return controller.login(data)

    @blueprint.route("/register", methods=["POST"])
    def register():
        data = request.json
        return controller.register(data)

    @blueprint.route("/profile", methods=["GET"])
    @token_required
    def profile(current_user):
        return controller.profile(current_user)

    return blueprint
