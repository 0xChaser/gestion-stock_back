from pydantic import PostgresDsn, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Sequence

class Settings(BaseSettings):
    db_url: PostgresDsn
    origins: Sequence[str] = ["*"]
    
    
    model_config = SettingsConfigDict(env_file=".env")
    

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()