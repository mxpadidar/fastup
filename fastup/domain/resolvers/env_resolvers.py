import os
import pathlib


def resolve_path_env(env: str, fallback: pathlib.Path) -> pathlib.Path:
    """
    Resolve a path from an environment variable or fallback.

    :param env: Name of the environment variable.
    :param fallback: Fallback path if the environment variable is not set.
    :return: Resolved and validated path.
    :raises FileNotFoundError: If the resolved path does not exist.
    """
    value = os.getenv(env)
    path = pathlib.Path(value).resolve() if value else fallback.resolve()
    if not path.exists():
        raise FileNotFoundError(f"path does not exist: {path}")
    return path


def resolve_str_env(env: str, fallback: str | None = None) -> str:
    """
    Resolve a string from an environment variable or fallback.

    :param env: Name of the environment variable.
    :param fallback: Fallback value if the environment variable is not set.
    :return: String value from the environment or fallback.
    :raises ValueError: If neither environment variable nor fallback is available.
    """
    value = os.getenv(env)
    if value is None:
        if fallback is None:
            raise ValueError(f"{env=} is not set and no fallback provided")
        return fallback
    return value


def resolve_int_env(env: str, fallback: int | None = None) -> int:
    """
    Resolve an integer from an environment variable or fallback.

    :param env: Name of the environment variable.
    :param fallback: Fallback integer if the environment variable is not set.
    :return: Integer value from the environment or fallback.
    :raises ValueError: If conversion fails or both are missing.
    """
    value = os.getenv(env)
    if value is None:
        if fallback is None:
            raise ValueError(f"{env=} is not set and no fallback provided")
        return fallback

    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"{env} is not a valid integer: {value}") from e
