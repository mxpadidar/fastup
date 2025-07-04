import os
import pathlib
from typing import TypeVar

from dotenv import load_dotenv

from fastup.core.errors import NotFoundErr, ValidationErr
from fastup.core.logger import get_logger

logger = get_logger("fastup.envlib")


def loadenv(path: pathlib.Path) -> None:
    """load environment variables from a .env file."""

    logger.debug("loading dotenv file from %s", path)
    if not path.exists():
        logger.error("dotenv file not found at %s", path)
        raise NotFoundErr

    load_dotenv(path)


T = TypeVar("T")


def getenv(key: str, fallback: T) -> T:
    """Get an environment variable with a fallback value."""
    var = os.getenv(key, fallback)
    if isinstance(fallback, str):
        return str(var)  # type: ignore
    elif isinstance(fallback, bool):
        if var in (True, "1", "true", "True"):
            return True  # type: ignore
        elif var in (False, "0", "false", "False"):
            return False  # type: ignore
    elif isinstance(fallback, int):
        try:
            return int(var)  # type: ignore
        except Exception:
            pass
    logger.error("invalid fallback type for getenv: %s.", type(fallback))
    raise ValidationErr
