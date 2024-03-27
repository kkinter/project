from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(".env")


class Settings(BaseSettings):
    app_name: str = "octo API"
    JWT_SECRET: str
    JWT_ALGORITHM: str
    PORT: str
    NUTRITIONIX_API_ID: str
    NUTRITIONIX_API_KEY: str
    NUTRITIONIX_URL: str
    EXPECTED_CALORIES_PER_DAY: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
