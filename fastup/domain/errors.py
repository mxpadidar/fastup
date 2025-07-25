import pathlib


class BaseErr(Exception):
    """base class for all custom exceptions"""

    def __init__(self, message: str) -> None:  # pragma: no cover
        super().__init__(message)
        self.message = message


class FileParseErr(Exception):
    """custom exception for file parsing errors."""

    def __init__(self, path: pathlib.Path) -> None:
        super().__init__(f"could not parse file. {path=}")
        self.path = path
