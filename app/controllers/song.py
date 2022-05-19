from flask import Response, Request, jsonify
from http import HTTPStatus
from typing import List, Tuple

from app.models.song import Song
from app.models.user import User
from app.services.song import SongService


class SongController:
    def __init__(self, service: SongService):
        self.service = service

    def create(self, request: Request, current_user: User) -> Tuple[Response, int]:
        try:
            song_file = request.files["song_file"]
            data = request.form.to_dict()
            data["user_id"] = current_user.id
            self.service.create(song_file, data)
            return "", HTTPStatus.OK
        except Exception:
            return "", HTTPStatus.INTERNAL_SERVER_ERROR

    def update(self, request: Request) -> Tuple[Response, int]:
        try:
            song_id = int(request.view_args["song_id"])
            song = self.service.update(song_id, request.json)
            return jsonify(song), HTTPStatus.OK
        except Exception as e:
            return "", HTTPStatus.INTERNAL_SERVER_ERROR

    def delete(self, request: Request) -> Tuple[Response, int]:
        try:
            song_id = int(request.view_args["song_id"])
            self.service.delete(song_id)
            return "", HTTPStatus.OK
        except Exception as e:
            return "", HTTPStatus.INTERNAL_SERVER_ERROR

    def get_all(self, request: Request) -> Tuple[List[Song], int]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        return (
            jsonify({"songs": self.service.get_all(take, skip)}),
            HTTPStatus.OK,
        )

    def get_by_id(self, request: Request) -> Tuple[Song, int]:
        song_id = int(request.view_args["song_id"])

        return (
            jsonify(self.service.get_by_id(song_id)),
            HTTPStatus.OK,
        )
