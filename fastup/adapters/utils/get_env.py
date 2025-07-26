import os
import pathlib


def get_env_path(env_var: str, fallback: pathlib.Path) -> pathlib.Path:
    """
    resolve a path from an env var or fallback;
    raises FileNotFoundError if the path does not exist.
    """
    value = os.getenv(env_var)
    path = pathlib.Path(value).resolve() if value else fallback.resolve()
    if not path.exists():
        raise FileNotFoundError(f"path does not exist: {path}")
    return path


def get_env_str(env: str, fallback: str | None = None) -> str:
    """return the value of an environment variable or a fallback."""
    value = os.getenv(env)
    if value is None:
        if fallback is None:
            raise ValueError
        return fallback
    return value


def get_env_int(env: str, fallback: int | None = None) -> int:
    """return the integer value of an environment variable or a fallback."""
    value = os.getenv(env)
    if value is None:
        if fallback is None:
            raise ValueError
        return fallback

    try:
        return int(value)
    except ValueError as e:
        raise ValueError from e
