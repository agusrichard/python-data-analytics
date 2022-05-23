from typing import Callable, List, Dict
from werkzeug.datastructures import FileStorage

from app.models.user import User
from app.common.file import renaming_file
from app.common.messages import SONG_NOT_FOUND
from app.repositories.song import SongRepository
from app.common.exceptions import NotFoundException, FieldRequired, Unauthorized


class SongService:
    def __init__(self, repository: SongRepository, upload_file: Callable) -> None:
        self.repository = repository
        self.upload_file = upload_file

    def create(self, files: Dict[str, FileStorage], song_data: dict) -> dict:
        if "title" not in song_data or not song_data:
            raise FieldRequired("title")

        if "song_file" not in files or not files["song_file"]:
            raise FieldRequired("song_file")

        for key, file in files.items():
            if file.filename == "":
                continue  # skip not required fields/files

            file.filename = renaming_file(file.filename)
            key_data = key.replace("file", "url")
            song_data[key_data] = self.upload_file(file)

        return self.repository.create(song_data)

    def update(
        self,
        current_user: User,
        song_id: int,
        files: Dict[str, FileStorage],
        song_data: dict,
    ) -> dict:
        song = self.repository.get_by_id(song_id)
        if song is None:
            raise NotFoundException(SONG_NOT_FOUND)

        if current_user.id != song.user_id:
            raise Unauthorized()

        for key, file in files.items():
            if file.filename == "":
                continue  # skip not required fields/files

            file.filename = renaming_file(file.filename)
            key_data = key.replace("file", "url")
            song_data[key_data] = self.upload_file(file)

        return self.repository.update(song, song_data)

    def delete(self, current_user: User, song_id: int) -> None:
        song = self.repository.get_by_id(song_id)
        if song is None:
            raise NotFoundException(SONG_NOT_FOUND)

        if current_user.id != song.user_id:
            raise Unauthorized()

        self.repository.delete(song)

    def get_by_id(self, song_id: int) -> dict:
        song = self.repository.get_by_id(song_id)
        if song is None:
            raise NotFoundException(SONG_NOT_FOUND)

        return song.to_dict()

    def get_all(self, take: int = 10, skip: int = 0) -> List[dict]:
        songs = self.repository.get_all(take, skip)
        return [song.to_dict() for song in songs]
