from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify, current_app

from app.services.auth import AuthService
from app.common.exceptions import BadRequestException, NotFoundException


def create_auth_handlers(service: AuthService, decorators: dict):
    blueprint = Blueprint("auth", __name__)
    token_required = decorators["token_required"]

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
            result = service.login(data)
            print("result", result)
            return jsonify(result), HTTPStatus.OK
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

    @blueprint.route("/profile", methods=["GET"])
    @token_required
    def profile(current_user):
        return jsonify(current_user.to_dict())

    return blueprint
