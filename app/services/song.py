import base64
from flask import Flask
from threading import Thread
from typing import Callable, List, Dict
from werkzeug.datastructures import FileStorage

from app.models.user import User
from app.common.file import renaming_file
from app.repositories.song import SongRepository
from app.common.exceptions import (
    NotFoundException,
    UnauthorizedException,
    FieldRequiredException,
)
from app.common.messages import (
    SONG_NOT_FOUND,
    UNAUTHORIZED_TO_DELETE_SONG,
    UNAUTHORIZED_TO_UPDATE_SONG,
)


class SongService:
    def __init__(
        self, app: Flask, repository: SongRepository, upload_file: Callable
    ) -> None:
        self.app = app
        self.repository = repository
        self.upload_file = upload_file

    def create(self, files: Dict[str, FileStorage], song_data: dict) -> None:
        if "title" not in song_data or not song_data:
            raise FieldRequiredException("title")

        if "song_file" not in files or not files["song_file"]:
            raise FieldRequiredException("song_file")

        files = self.__preprocess_files(files)
        thread = Thread(target=self.__create, args=(files, song_data))
        thread.start()

    def __create(self, files: dict, song_data: dict) -> None:
        with self.app.app_context():
            for key, file in files.items():
                key_data = key.replace("file", "url")
                song_data[key_data] = self.upload_file(file)

            self.repository.create(song_data)

    def update(
        self,
        current_user: User,
        song_id: int,
        files: Dict[str, FileStorage],
        song_data: dict,
    ) -> None:
        song = self.repository.get_by_id(song_id)
        if song is None:
            raise NotFoundException(SONG_NOT_FOUND)

        if current_user.id != song.user_id:
            raise UnauthorizedException(UNAUTHORIZED_TO_UPDATE_SONG)

        files = self.__preprocess_files(files)
        thread = Thread(target=self.__update, args=(song_id, files, song_data))
        thread.start()

    def __update(self, song_id: int, files: dict, song_data: dict) -> None:
        with self.app.app_context():
            for key, file in files.items():
                key_data = key.replace("file", "url")
                song_data[key_data] = self.upload_file(file)

            song = self.repository.get_by_id(song_id)
            self.repository.update(song, song_data)

    def delete(self, current_user: User, song_id: int) -> None:
        song = self.repository.get_by_id(song_id)
        if song is None:
            raise NotFoundException(SONG_NOT_FOUND)

        if current_user.id != song.user_id:
            raise UnauthorizedException(UNAUTHORIZED_TO_DELETE_SONG)

        self.repository.delete(song)

    def get_by_id(self, song_id: int) -> dict:
        song = self.repository.get_by_id(song_id)
        if song is None:
            raise NotFoundException(SONG_NOT_FOUND)

        return song.to_dict()

    def get_all(self, take: int = 10, skip: int = 0) -> List[dict]:
        songs = self.repository.get_all(take, skip)
        return [song.to_dict() for song in songs]

    @staticmethod
    def __preprocess_files(files: Dict[str, FileStorage]) -> dict:
        result = {}

        for key, file in files.items():
            if file is None or file.filename == "":
                continue  # skip not required fields/files

            result[key] = {
                "stream": base64.b64encode(file.stream.read()),
                "name": file.name,
                "filename": renaming_file(file.filename),
                "content_type": file.content_type,
                "content_length": file.content_length,
                "headers": {header[0]: header[1] for header in file.headers},
            }

        return result
