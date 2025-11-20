from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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

    model_config = SettingsConfigDict(env_file=".env", env_prefix="fastup_")


# A single, globally accessible instance of the settings.
# Import this object into any module that needs access to configuration.
settings = Settings()
