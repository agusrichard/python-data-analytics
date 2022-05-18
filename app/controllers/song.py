from flask import Response, Request, jsonify
from http import HTTPStatus
from typing import List, Tuple

from app.models.song import Song
from app.services.song import SongService


class SongController:
    def __init__(self, service: SongService):
        self.service = service

    def create(self, request: Request) -> Tuple[Response, int]:
        try:
            song = self.service.create(request.json)
            return jsonify(song), HTTPStatus.OK
        except Exception as e:
            return jsonify(e.to_dict()), e.error_code

    def update(self, request: Request) -> Tuple[Response, int]:
        try:
            song_id = int(request.view_args["song_id"])
            song = self.service.update(song_id, request.json)
            return jsonify(song), HTTPStatus.OK
        except Exception as e:
            return jsonify(e.to_dict()), e.error_code

    def delete(self, request: Request) -> Tuple[Response, int]:
        try:
            song_id = int(request.view_args["song_id"])
            self.service.delete(song_id)
            return "", HTTPStatus.OK
        except Exception as e:
            return jsonify(e.to_dict()), e.error_code

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
