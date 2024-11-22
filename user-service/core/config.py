from pathlib import Path

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"


class AppConfig(BaseConfig):
    VERSION: str = "1.0.1"
    POSTGRES_URL: str
    TEST_POSTGRES_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int = 60 * 24


config: AppConfig = AppConfig()
