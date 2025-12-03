import datetime
import functools
import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class PydanticConfig(BaseSettings):
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

    # --- OTP Configuration ---
    otp_length: int = 4
    otp_lifetime_sec: int = 300  # 5 minutes
    otp_max_attempts: int = 3
    otp_rate_limit_max_requests: int = 5
    otp_rate_limit_window_sec: int = 600  # 10 minutes

    # --- JWT Configuration ---
    jwt_secret_key: str = secrets.token_urlsafe(32)
    signup_token_ttl_sec: int = 900  # 15 minutes

    # --- Computed fields that implement the CoreConf protocol ---
    @property
    def otp_lifetime(self) -> datetime.timedelta:  # pragma: no cover
        """Derived timedelta object for OTP lifetime."""
        return datetime.timedelta(seconds=self.otp_lifetime_sec)

    @property
    def otp_rate_limit_window(self) -> datetime.timedelta:  # pragma: no cover
        """Derived timedelta object for the rate-limit window."""
        return datetime.timedelta(seconds=self.otp_rate_limit_window_sec)

    @property
    def signup_token_ttl(self) -> datetime.timedelta:  # pragma: no cover
        """Derived timedelta object for signup token TTL."""
        return datetime.timedelta(seconds=self.signup_token_ttl_sec)

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="fastup_", frozen=True
    )


@functools.cache
def get_config() -> PydanticConfig:
    """Provides a singleton instance of the application configuration."""
    return PydanticConfig()
