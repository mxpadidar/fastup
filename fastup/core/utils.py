import os
import pathlib
import tomllib
from typing import Type, TypedDict, Unpack


class TomlFileDoesNotExistError(Exception):
    def __init__(self, path: pathlib.Path):
        super().__init__(f"TOML file does not exist: {path}")
        self.path = path


class DatabaseDsnError(Exception):
    def __init__(self, message: str = "Database DSN could not be generated"):
        super().__init__(message)


def load_toml(path: pathlib.Path) -> dict:
    """
    Load a TOML file and return its contents as a dictionary.
    """
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        raise TomlFileDoesNotExistError(path)


class DatabaseConfig(TypedDict):
    db_name: str
    host: str
    port: int
    user: str
    password: str


def get_database_dsn(**defaults: Unpack[DatabaseConfig]) -> str:
    """
    generate a database DSN (Data Source Name) string
    if envinronment variables are not set, use the defaults provided
    """
    from os import getenv

    try:
        db_name = getenv("POSTGRES_DB", defaults["db_name"])
        host = getenv("POSTGRES_HOST", defaults["host"])
        port = getenv("POSTGRES_PORT", defaults["port"])
        user = getenv("POSTGRES_USER", defaults["user"])
        password = getenv("POSTGRES_PASSWORD", defaults["password"])
    except KeyError as e:
        raise DatabaseDsnError("Missing required database configuration") from e

    if any(v is None for v in [db_name, host, port, user, password]):
        raise DatabaseDsnError("Incomplete database configuration")

    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"


def get_env_variable[T](key: str, default: T | None = None, cast: Type = str) -> T:
    val = os.getenv(key, default)
    if cast and val is not None:
        return cast(val)
    return cast(val)


def get_bool_env(key: str, default: bool = False) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes", "on")


def another_function():
    """
    This is a placeholder for another function that might be used in the future.
    """
    pass
