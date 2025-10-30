import typing


class AppConfig(typing.TypedDict):
    title: str
    version: str


class ServerConfig(typing.TypedDict):
    host: str
    port: int
    debug: bool


class DBConfig(typing.TypedDict):
    url: str
    echo: bool
    pool_size: int
    max_overflow: int
    pool_timeout: int  # seconds
