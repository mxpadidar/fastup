import typing


class BaseErr(Exception):
    """Base exception class for the application.

    :param message: Optional error message
    :param code: Optional error code
    :param extra: Optional extra data
    """

    message: str = "Something went wrong"
    code: int = 500
    extra: dict[str, typing.Any] = {}

    def __init__(self, message=None, code=None, extra=None) -> None:
        self.message: str = message or self.message
        self.code = code or self.code
        self.extra = extra or self.extra
        super().__init__(self.message)


class NotFoundErr(BaseErr):
    """Raised when a resource is not found."""

    message = "Not found"
    code = 404


class UoWIsNotReady(BaseErr):
    """Raised when UoW operations are attempted outside the context manager."""

    message = "UoW not ready"
    code = 500


class ValidationErr(BaseErr):
    """Raised when validation fails."""

    message = "Validation error"
    code = 422
