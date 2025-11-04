import typing
from http import HTTPStatus


class BaseExc(Exception):
    """Base exception for the application.

    Designed to be the parent of all domain / HTTP-aware exceptions.

    :param message: Human-readable error message.
    :param code: HTTP status code (int or HTTPStatus) representing this error.
    :param extra: Optional additional data attached to the error.
    """

    message: str = "Something went wrong"
    code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    extra: dict[str, typing.Any] = {}

    def __init__(
        self,
        message: str | None = None,
        code: int | None = None,
        extra: dict[str, typing.Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.code = code or self.code
        self.extra = extra or self.extra
        super().__init__(self.message)


class LogicalExc(BaseExc):
    """Raised for internal logic/contract errors (programmer mistakes)"""

    message = "Internal logic error"
    code = HTTPStatus.INTERNAL_SERVER_ERROR


class NotFoundExc(BaseExc):
    """Raised when a requested resource cannot be found."""

    message = "Resource not found"
    code = HTTPStatus.NOT_FOUND
