from http import HTTPStatus
from typing import List, Tuple, Optional
from flask import Response, Request, jsonify

from app.models.song import Song
from app.models.user import User
from app.services.song import SongService
from app.common.exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    UploadFailedException,
    FieldRequiredException,
)


class SongController:
    def __init__(self, service: SongService):
        self.service = service

    def create(self, current_user: User, request: Request) -> Tuple[Response, int]:
        try:
            files = {
                "song_file": request.files.get("song_file", None),
                "small_thumbnail_file": request.files.get("small_thumbnail_file", None),
                "large_thumbnail_file": request.files.get("large_thumbnail_file", None),
            }
            data = request.form.to_dict()
            data["user_id"] = current_user.id
            self.service.create(files, data)
            return "", HTTPStatus.CREATED
        except FieldRequiredException as e:
            return jsonify(e.to_dict()), e.error_code
        except UploadFailedException as e:
            return jsonify(e.to_dict()), e.error_code
        except BadRequestException as e:
            return jsonify(e.to_dict()), e.error_code

    def update(
        self, current_user: User, request: Request, song_id: Optional[int]
    ) -> Tuple[Response, int]:
        try:
            if song_id is None:
                err = FieldRequiredException("song_id")
                return jsonify(err.to_dict()), err.error_code

            song_id = int(song_id)
            files = {}
            for key, file in request.files.items():
                files[key] = file

            self.service.update(current_user, song_id, files, request.form.to_dict())
            return "", HTTPStatus.OK
        except UnauthorizedException as e:
            return jsonify(e.to_dict()), e.error_code
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code
        except UploadFailedException as e:
            return jsonify(e.to_dict()), e.error_code
        except BadRequestException as e:
            return jsonify(e.to_dict()), e.error_code

    def delete(
        self, current_user: User, song_id: Optional[int]
    ) -> Tuple[Response, int]:
        try:
            if song_id is None:
                err = FieldRequiredException("song_id")
                return jsonify(err.to_dict()), err.error_code

            self.service.delete(current_user, song_id)
            return "", HTTPStatus.OK
        except UnauthorizedException as e:
            return jsonify(e.to_dict()), e.error_code
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code

    def get_all(self, request: Request) -> Tuple[List[Song], int]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        return jsonify(self.service.get_all(take, skip)), HTTPStatus.OK

    def get_by_id(self, song_id: Optional[int]) -> Tuple[Song, int]:
        try:
            if song_id is None:
                err = FieldRequiredException("song_id")
                return jsonify(err.to_dict()), err.error_code

            song = self.service.get_by_id(song_id)
            return jsonify(song), HTTPStatus.OK
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code
