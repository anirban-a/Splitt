from fastapi import Depends
from pymongo.collection import Collection


from models import User


class UserRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def save(self, user: User):
        self.collection.insert_one(user.model_dump())