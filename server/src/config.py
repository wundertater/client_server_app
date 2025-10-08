import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "mydatabase"
    DB_USER: str = "myuser"
    DB_PASSWORD: str = "mypassword"
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))


settings = Settings()


def get_async_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


def get_sync_db_url():
    return (
        f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
