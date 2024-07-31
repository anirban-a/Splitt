from functools import lru_cache

from fastapi import APIRouter, Depends
from pymongo import MongoClient, database
from pymongo.collection import Collection

from config.config import BaseConfig
# from config.database import get_user_collection
from models import User
from repositories.user_repository import UserRepository
from services.user_service import UserService

router = APIRouter()


@lru_cache
def get_settings():
    return BaseConfig()


def get_db(base_config: BaseConfig = Depends(get_settings)) -> database.Database:
    client = MongoClient(base_config.MONGO_URL)
    return client.get_database(base_config.DATABASE_NAME)


def get_user_collection(db: database.Database = Depends(get_db)) -> Collection:
    return db.get_collection('user')


def get_user_repository(user_collection: Collection = Depends(get_user_collection)):
    return UserRepository(user_collection)


def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)


@router.post("/user")
async def root(user: User, user_service: UserService = Depends(get_user_service)):
    _user = user_service.create_user(user)
    return {"user": _user}
