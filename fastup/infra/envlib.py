import logging
import os
import pathlib
from typing import cast

logger = logging.getLogger(__name__)


def loadenv(path: pathlib.Path) -> None:
    """load environment variables from a .env file."""
    from dotenv import load_dotenv

    if not path.exists():
        raise FileNotFoundError

    load_dotenv(path)


def getenv[T](key: str, fallback: T) -> T:
    """Get an environment variable and cast it to the fallback type."""

    envar = os.getenv(key)

    if envar is None and fallback is not None:
        return fallback

    if envar is None:
        raise ValueError(f"environment variable {key} not set.")

    if type(fallback) is str:
        envar = str(envar)

    elif type(fallback) is bool:
        val = envar.strip().lower()
        if val in ("1", "true"):
            envar = True
        elif val in ("0", "false"):
            envar = False
        else:
            raise ValueError(f"environment variable {key} is not a valid boolean.")

    elif type(fallback) is int:
        try:
            envar = int(envar)
        except ValueError:
            raise ValueError(f"environment variable {key} is not a valid integer.")

    elif type(fallback) is float:
        try:
            envar = float(envar)
        except ValueError:
            raise ValueError(f"environment variable {key} is not a valid float.")

    else:
        raise TypeError(
            f"unsupported type {type(fallback)} for environment variable {key}."
        )

    return cast(T, envar)
