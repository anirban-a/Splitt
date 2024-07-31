import logging

from models import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.logger = logging.getLogger(__name__)
        self.user_repo = user_repo

    def create_user(self, user: User):
        # self.logger.info(f"Saving user:\n {user}")
        self.logger.info("Saved User")
        self.user_repo.save(user)
        return user
