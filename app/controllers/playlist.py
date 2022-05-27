from http import HTTPStatus
from typing import Tuple, Optional
from flask import Response, jsonify, request

from app.models.user import User
from app.services.playlist import PlaylistService
from app.common.exceptions import (
    NotFoundException,
    UnauthorizedException,
    FieldRequiredException,
)


class PlaylistController:
    def __init__(self, service: PlaylistService) -> None:
        self.service = service

    def create(self, current_user: User) -> Tuple[Response, int]:
        try:
            data = request.form.to_dict()
            data["user_id"] = current_user.id
            self.service.create(data)
            return "", HTTPStatus.CREATED
        except FieldRequiredException as e:
            return jsonify(e.to_dict()), e.error_code

    def update(
        self, current_user: User, playlist_id: Optional[int]
    ) -> Tuple[Response, int]:
        try:
            if playlist_id is None:
                err = FieldRequiredException("playlist_id")
                return jsonify(err.to_dict()), err.error_code

            playlist_id = int(playlist_id)
            data = request.form.to_dict()
            self.service.update(current_user, playlist_id, data)
            return "", HTTPStatus.OK
        except UnauthorizedException as e:
            return jsonify(e.to_dict()), e.error_code
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code

    def delete(
        self, current_user: User, playlist_id: Optional[int]
    ) -> Tuple[Response, int]:
        try:
            if playlist_id is None:
                err = FieldRequiredException("playlist_id")
                return jsonify(err.to_dict()), err.error_code

            playlist_id = int(playlist_id)
            self.service.delete(current_user, playlist_id)
            return "", HTTPStatus.OK
        except UnauthorizedException as e:
            return jsonify(e.to_dict()), e.error_code
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code

    def get_all(self, *args) -> Tuple[Response, int]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        return jsonify(self.service.get_all(take, skip)), HTTPStatus.OK

    def get_by_id(self, _, playlist_id: Optional[int]) -> Tuple[Response, int]:
        take = request.args.get("take", 10, int)
        skip = request.args.get("skip", 0, int)

        try:
            if playlist_id is None:
                err = FieldRequiredException("playlist_id")
                return jsonify(err.to_dict()), err.error_code

            playlist = self.service.get_by_id(playlist_id, take, skip)
            return jsonify(playlist), HTTPStatus.OK
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code

    def add_song(self, current_user: User, playlist_id: int, song_id: int):
        try:
            self.service.add_song(current_user, playlist_id, song_id)
            return "", HTTPStatus.OK
        except UnauthorizedException as e:
            return jsonify(e.to_dict()), e.error_code
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code

    def remove_song(self, current_user: User, playlist_id: int, song_id: int):
        try:
            self.service.remove_song(current_user, playlist_id, song_id)
            return "", HTTPStatus.OK
        except UnauthorizedException as e:
            return jsonify(e.to_dict()), e.error_code
        except NotFoundException as e:
            return jsonify(e.to_dict()), e.error_code
