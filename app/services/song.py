from typing import List

from app.repositories.song import SongRepository


class SongService:
    def __init__(self, repository: SongRepository) -> None:
        self.repository = repository

    def create(self, song: dict) -> dict:
        return self.repository.create(song)

    def update(self, song_id: int, song: dict) -> dict:
        return self.repository.update(song_id, song)

    def delete(self, song_id: int) -> None:
        self.repository.delete(song_id)

    def get_by_id(self, song_id: int) -> dict:
        return self.repository.get_by_id(song_id)

    def get_all(self, take: int = 10, skip: int = 0) -> List[dict]:
        return self.repository.get_all(take, skip)
