# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    MONGO_URL: str
    DATABASE_NAME: str

    class Config:
        env_file = ".env"
