from http import HTTPStatus
from typing import List, Tuple, Optional
from flask import Response, Request, jsonify

from app.models.song import Song
from app.models.user import User
from app.services.song import SongService


class SongController:
    def __init__(self, service: SongService):
        self.service = service

    def create(self, request: Request, current_user: User) -> Tuple[Response, int]:
        try:
            files = {
                "song_file": request.files["song_file"],
                "small_thumbnail_file": request.files["small_thumbnail_file"],
                "large_thumbnail_file": request.files["large_thumbnail_file"],
            }
            data = request.form.to_dict()
            data["user_id"] = current_user.id
            self.service.create(files, data)
            return "", HTTPStatus.OK
        except Exception:
            return "", HTTPStatus.INTERNAL_SERVER_ERROR

    def update(self, song_id: Optional[int], request: Request) -> Tuple[Response, int]:
        try:
            if song_id is None:
                return "", HTTPStatus.BAD_REQUEST

            song_id = int(song_id)
            files = {}
            for key, file in request.files.items():
                files[key] = file
            song = self.service.update(song_id, files, request.form.to_dict())
            return jsonify(song), HTTPStatus.OK
        except Exception as e:
            print("Exception:", e)
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
