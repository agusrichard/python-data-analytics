from datetime import datetime

from repositories.auth import AuthRepository
from common.exceptions import NotFoundException, BadRequestException


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def login(self, data: dict):
        user = self.repository.get_by_email(data["email"])
        if not user:
            raise NotFoundException("User not found")

        if not user.check_password(data["password"]):
            raise BadRequestException("Wrong email or password")

        data = user.to_dict()
        data["last_login"] = datetime.utcnow()
        self.repository.update(user.id, data)
        return "Login inside service"

    def register(self, data: dict):
        self.repository.create(data)
