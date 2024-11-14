from pydantic_settings import BaseSettings


class ConfigSettings(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = "../.env"
        env_file_encoding = "utf-8"


class Config(ConfigSettings):
    POSTGRES_URL: str
    TEST_POSTGRES_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int = 60 * 24


config: Config = Config()
