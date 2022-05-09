from flask import Blueprint


from services.auth import AuthService


def init_auth_handlers(service: AuthService):
    blueprint = Blueprint("auth", __name__)

    @blueprint.route("/login")
    def login():
        return service.login()

    @blueprint.route("/register")
    def register():
        return service.register()

    return blueprint
