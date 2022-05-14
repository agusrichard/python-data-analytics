from typing import Tuple, List

from app.models.user import User
from app.common.messages import USER_NOT_FOUND
from app.repositories.user import UserRepository
from app.common.exceptions import NotFoundException


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def follow(self, from_id: int, to_id: int):
        from_user, to_user = self.__get_from_to_users(from_id, to_id)
        self.repository.follow(from_user, to_user)

    def unfollow(self, from_id: int, to_id: int):
        from_user, to_user = self.__get_from_to_users(from_id, to_id)
        self.repository.unfollow(from_user, to_user)

    def get_followers(self, user_id: int, take: 10, skip: 0) -> List[User]:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundException(USER_NOT_FOUND)

        return user.get_followers(take, skip)

    def get_followed_users(self, user_id: int, take: 10, skip: 0) -> List[User]:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundException(USER_NOT_FOUND)

        return user.get_followed_users(take, skip)

    def __get_from_to_users(self, from_id: int, to_id: int) -> Tuple[User, User]:
        from_user = self.repository.get_by_id(from_id)
        to_user = self.repository.get_by_id(to_id)
        if from_user is None or to_user is None:
            raise NotFoundException(USER_NOT_FOUND)

        return from_user, to_user
