from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"

    secret_key: str = "replace-me"

    database_url: str = "sqlite:///./pocketsmart.db"

    gemini_api_key: str | None = None

    gemini_model: str = "gemini-2.5-flash"

    access_token_expire_minutes: int = 1440

    max_upload_mb: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()