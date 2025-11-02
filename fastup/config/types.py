import datetime
import typing


class AppConf(typing.TypedDict):
    name: str
    version: str


class ServerConf(typing.TypedDict):
    host: str
    port: int
    debug: bool


class DBConfig(typing.TypedDict):
    url: str
    echo: bool
    pool_size: int
    max_overflow: int
    pool_timeout: int  # seconds


class RefreshTokenRotationConfig(typing.TypedDict):
    """Per-session refresh token rotation rate-limiting."""

    burst_limit: int  # Maximum number of rotations allowed within the burst_window.
    burst_window: datetime.timedelta  # Time window over which burst_limit is measured.
    lock: datetime.timedelta  # Duration to block when burst_limit is exceeded.
    cooldown: datetime.timedelta  # minimal gap between rotations
