from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(".env")


class Settings(BaseSettings):
    app_name: str = "octo API"
    JWT_SECRET: str
    JWT_ALGORITHM: str
    PORT: str

    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
