from repositories.auth import AuthRepository


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def login(self):
        return "Login inside service"

    def register(self):
        return "Register inside service"
