from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    secret_key: str = "default_secret_key"
    log_level: str = "debug"
    debug: bool = False

    title: str = "fastup"
    version: str = "0.1.0"

    host: str = "127.0.0.1"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_prefix="fastup_",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """get the settings instance.
    uses lru cache to avoid reloading settings multiple times."""
    return Settings()
