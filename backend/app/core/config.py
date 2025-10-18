from functools import lru_cache
from typing import Any

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    PROJECT_NAME: str = "Malware Psychology Backend"
    DATABASE_URL: PostgresDsn | None = None
    JWT_SECRET: str = "changeme"
    JWT_ALGO: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_origins(cls, value: Any) -> list[AnyHttpUrl] | Any:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
