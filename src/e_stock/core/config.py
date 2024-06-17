from functools import lru_cache
from typing import Sequence

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: PostgresDsn
    origins: Sequence[str] = ["*"]
    secret_key: SecretStr
    token_lifetime_in_seconds: int = 3600

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
