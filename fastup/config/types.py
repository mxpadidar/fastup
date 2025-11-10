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


class RedisConfig(typing.TypedDict):
    host: str
    port: int
    db: int
    password: typing.NotRequired[str]
