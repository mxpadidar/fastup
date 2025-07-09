class BaseErr(Exception):
    def __init__(self, detail: str, context: dict | None = None) -> None:
        """
        Base class for all custom exceptions in the application.
        :param detail: A detailed message about the error.
        :param context: Optional additional context about the error.
        """
        super().__init__(detail)
        self.detail = detail
        self.context = context


class ServerErr(BaseErr): ...
