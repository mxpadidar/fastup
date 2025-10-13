import os


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
