import logging

from models import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.logger = logging.getLogger(__name__)
        self.user_repo = user_repo

    def create_user(self, user: User) -> User:
        # self.logger.info(f"Saving user:\n {user}")
        self.logger.info("Saved User")
        result = self.user_repo.save(user)
        inserted_id = str(result.inserted_id)

        return self.user_repo.find_by_id(inserted_id)

    def find_by_id(self, user_id: str) -> User:
        return self.user_repo.find_by_id(user_id)
