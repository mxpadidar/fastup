import typing


class BaseExc(Exception):
    message: str = "An unexpected application error occurred."
    extra: dict[str, typing.Any]

    def __init__(self, message: str | None = None, extra: dict | None = None) -> None:
        self.message = message or self.message
        self.extra = extra or dict()
        super().__init__(self.message)


class InternalExc(BaseExc):
    message = "An unexpected internal error occurred."


class NotFoundExc(BaseExc):
    message = "The requested resource could not be found."


class ConflictExc(BaseExc):
    message = "A resource conflict occurred, likely due to a duplicate entry."


class UnitOfWorkContextExc(InternalExc):
    message = "An operation was attempted outside of the active Unit of Work context."


class SmsSendFailed(BaseExc):
    message = "Failed to send SMS message."


class AccessDeniedExc(BaseExc):
    message = "Access to the requested resource is denied."


class AttemptLimitReached(BaseExc):
    message = "The maximum number of allowed attempts has been reached."
