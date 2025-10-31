import typing


class AppConf(typing.TypedDict):
    name: str
    version: str


class ServerConf(typing.TypedDict):
    host: str
    port: int
    debug: bool
