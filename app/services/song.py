from datetime import datetime
from typing import Callable, List
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from app.repositories.song import SongRepository


class SongService:
    def __init__(self, repository: SongRepository, upload_file: Callable) -> None:
        self.repository = repository
        self.upload_file = upload_file

    def create(self, file: FileStorage, song_data: dict) -> dict:
        uploaded_date = datetime.utcnow()
        splitted = file.filename.rsplit(".", 1)
        filename = splitted[0]
        file_extension = splitted[1]
        filename = secure_filename(filename.lower())
        filename = f"{uploaded_date.strftime('%Y%m%d%H%M%S')}--{filename}"
        filename = f"{filename}.{file_extension}"
        file.filename = filename
        song_url = self.upload_file(file)
        song_data["song_url"] = song_url
        return self.repository.create(song_data)

    def update(self, song_id: int, song: dict) -> dict:
        return self.repository.update(song_id, song)

    def delete(self, song_id: int) -> None:
        self.repository.delete(song_id)

    def get_by_id(self, song_id: int) -> dict:
        return self.repository.get_by_id(song_id)

    def get_all(self, take: int = 10, skip: int = 0) -> List[dict]:
        return self.repository.get_all(take, skip)
