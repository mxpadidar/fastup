import os

from fastup.core import errors


def get_str_env(key: str, default: str | None = None) -> str:
    val = os.getenv(key, default)
    if not val:
        raise errors.ValidationErr(
            msg=f"environment variable '{key}' is not set or is empty.",
        )

    return str(val)


def get_bool_env(key: str, default: bool = False) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes", "on")


def get_int_env(key: str, default: int = 0) -> int:
    val = os.getenv(key, default)
    try:
        return int(val)
    except ValueError:
        raise errors.ValidationErr(
            msg=f"environment variable '{key}' must be an integer.",
        )
