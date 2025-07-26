import os


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
