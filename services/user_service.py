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

        entity = self.user_repo.find_by_id(inserted_id)
        if entity:
            # entity['_id'] = inserted_id
            return User.from_mongo(**entity)
        raise Exception(f'User could not be created')
