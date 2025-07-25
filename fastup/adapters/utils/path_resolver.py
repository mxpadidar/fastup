import os
import pathlib


def resolve_path_from_env(
    env_var: str, default_path: pathlib.Path
) -> pathlib.Path:
    """returns a path from an environment variable or a default path."""
    from_env = os.getenv(env_var)
    if from_env:
        return pathlib.Path(from_env).resolve()
    return default_path.resolve()
