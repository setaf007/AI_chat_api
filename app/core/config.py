from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        )

    # App
    app_name: str = "AI Chat API"
    app_env: str = "local"

    # Security
    secret_key: str
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    # Database
    database_url: str

    # LMStudio
    lmstudio_base_url: AnyHttpUrl
    lm_studio_model: str

@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings so the .env is read once and reused.
    """
    return Settings()

settings = get_settings()