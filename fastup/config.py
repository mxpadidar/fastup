import functools
import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application settings

    Loaded from environment variables (e.g., `fastup_db_name=...`)
    or a .env file in the project root.
    """

    app_name: str = "Fastup"
    version: str = "0.1.0"
    debug: bool = True

    # --- Database Configuration ---
    # Defaults are set for the local development container.
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "fastup_dev"
    db_user: str = "fastup"
    db_password: str = "secret"

    # --- Database Pool Configuration ---
    db_pool_size: int = 5
    db_pool_timeout: int = 30
    db_pool_max_overflow: int = 10
    db_echo_sql: bool = False

    # --- Snowflake ID Generator Configuration ---
    snowflake_epoch: int = 1609459200000  # 2021-01-01 00:00:00 UTC in milliseconds
    snowflake_node_id: int = 1
    snowflake_worker_id: int = 1

    # --- Security Configuration ---
    hmac_secret_key: bytes = secrets.token_bytes(32)

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="fastup_", frozen=True
    )


@functools.cache
def get_config() -> Config:
    """Provides a singleton instance of the application configuration."""
    return Config()
