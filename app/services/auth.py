from datetime import datetime

from app.repositories.auth import AuthRepository
from app.common.exceptions import BadRequestException


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def login(self, data: dict) -> dict:
        user = self.repository.get_by_email(data["email"])
        if not user:
            raise BadRequestException("Wrong email or password")

        if not user.check_password(data["password"]):
            raise BadRequestException("Wrong email or password")

        data = user.to_dict()
        data["last_login"] = datetime.utcnow()
        self.repository.update(user.id, data)

        data["last_login"] = data["last_login"].isoformat()
        return {
            "user": data,
            "token": user.generate_token(),
        }

    def register(self, data: dict):
        self.repository.create(data)
