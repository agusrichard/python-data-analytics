from typing import Callable, List, Dict
from werkzeug.datastructures import FileStorage

from app.repositories.song import SongRepository
from app.common.file import renaming_file


class SongService:
    def __init__(self, repository: SongRepository, upload_file: Callable) -> None:
        self.repository = repository
        self.upload_file = upload_file

    def create(self, files: Dict[str, FileStorage], song_data: dict) -> dict:
        for key, file in files.items():
            file.filename = renaming_file(file.filename)
            key_data = key.replace("file", "url")
            song_data[key_data] = self.upload_file(file)

        return self.repository.create(song_data)

    def update(self, song_id: int, song: dict) -> dict:
        return self.repository.update(song_id, song)

    def delete(self, song_id: int) -> None:
        self.repository.delete(song_id)

    def get_by_id(self, song_id: int) -> dict:
        return self.repository.get_by_id(song_id)

    def get_all(self, take: int = 10, skip: int = 0) -> List[dict]:
        return self.repository.get_all(take, skip)
