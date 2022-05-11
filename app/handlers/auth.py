from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify

from app.services.auth import AuthService
from app.common.exceptions import BadRequestException, NotFoundException


def init_auth_handlers(service: AuthService):
    blueprint = Blueprint("auth", __name__)

    @blueprint.route("/login", methods=["POST"])
    def login():
        data = request.json
        if "email" not in data or "password" not in data:
            return (
                jsonify(
                    {
                        "message": "Email and password are required",
                        "error_code": HTTPStatus.BAD_REQUEST,
                    }
                ),
                HTTPStatus.BAD_REQUEST,
            )

        try:
            data = request.json
            service.login(data)
            return "", HTTPStatus.NO_CONTENT
        except BadRequestException as e:
            return jsonify(e.to_dict()), e.error_code
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code

    @blueprint.route("/register", methods=["POST"])
    def register():
        try:
            data = request.json
            service.register(data)
            return "", HTTPStatus.CREATED
        except IntegrityError:
            return (
                jsonify(
                    {
                        "message": "User already exists",
                        "error_code": HTTPStatus.CONFLICT,
                    }
                ),
                HTTPStatus.CONFLICT,
            )

    return blueprint
