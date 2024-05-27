from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    db_url: PostgresDsn
    
    model_config = SettingsConfigDict(env_file=".env")
    

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()