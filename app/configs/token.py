import jwt
from flask import Flask, jsonify, request
from typing import Callable
from functools import wraps

from app.models.user import User


def __token_required(app: Flask):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"][7:]

            if not token:
                return jsonify({"message": "a valid token is missing"})
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
                current_user = User.query.get(data["id"])
            except Exception as e:
                return jsonify({"message": "token is invalid"})

            return func(current_user, *args, **kwargs)

        return wrapper

    return decorator


def create_token_required_decorator(app: Flask):
    return __token_required(app)
