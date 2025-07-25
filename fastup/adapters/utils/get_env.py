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
