from flask import Blueprint

from app.common.token import token_required
from app.controllers.auth import AuthController


class AuthHandler:
    def __init__(self, controller: AuthController) -> None:
        self.__blueprint = Blueprint("auth", __name__)
        self.__blueprint.add_url_rule(
            "/login", "login", controller.login, methods=["POST"]
        )
        self.__blueprint.add_url_rule(
            "/register", "register", controller.register, methods=["POST"]
        )
        self.__blueprint.add_url_rule(
            "/profile", "profile", token_required(controller.profile), methods=["GET"]
        )

    @property
    def blueprint(self):
        return self.__blueprint
