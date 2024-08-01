from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from models import User


class UserRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def save(self, user: User) -> InsertOneResult:
        return self.collection.insert_one(user.model_dump())

    def find_by_id(self, id: str) -> User:
        entity = self.collection.find_one({'_id': ObjectId(id)})
        return User.from_mongo(**entity)
