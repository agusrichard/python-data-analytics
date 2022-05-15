import jwt
from http import HTTPStatus
from typing import Callable
from functools import wraps
from flask import jsonify, request, current_app

from app.models.user import User
from app.common.messages import TOKEN_INVALID, VALID_TOKEN_MISSING


def token_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"][7:]

        if not token:
            return (
                jsonify({"message": VALID_TOKEN_MISSING}),
                HTTPStatus.UNAUTHORIZED,
            )
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = User.query.get(data["id"])
        except Exception:
            return jsonify({"message": TOKEN_INVALID}), HTTPStatus.UNAUTHORIZED

        return func(current_user, *args, **kwargs)

    return wrapper
