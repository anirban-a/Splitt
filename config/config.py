# from pydantic import BaseSettings
from pydantic_settings import BaseSettings
import os

class BaseConfig(BaseSettings):
    MONGO_URL: str
    DATABASE_NAME: str

    class Config:
        is_prod = os.environ.get("ENVIRONMENT", "DEV") == 'PROD'
        env_file = ".env" if is_prod else ".dev_env"
