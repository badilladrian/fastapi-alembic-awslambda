import os
from pydantic import BaseSettings


class Settings(BaseSettings):

    SECRET_KEY: str

    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    API_HOST: str

    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str


settings = Settings()
