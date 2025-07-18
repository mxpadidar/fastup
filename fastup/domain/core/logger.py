from abc import ABC, abstractmethod


class Logger(ABC):
    """
    Abstract base class for structured, asynchronous logging.

    This class defines the interface for logging messages at different levels
    (info, error, debug) in an asynchronous environment.
    """

    def __init__(self, name: str) -> None:
        """Initialize the logger with a name."""
        self.name = name

    @abstractmethod
    async def info(self, message: str, **kwargs) -> None:
        """
        Asynchronously log an informational message.

        The message should be a format string
        (e.g., "User {user_id} logged in"),
        and keyword arguments will be used to fill in the placeholders.
        """
        ...

    @abstractmethod
    async def error(self, message: str, **kwargs) -> None:
        """
        Asynchronously log an error message.

        The message should be a format string
        (e.g., "Failed to process order {order_id}"),
        and keyword arguments will be used to fill in the placeholders.
        """
        ...

    @abstractmethod
    async def debug(self, message: str, **kwargs) -> None:
        """
        Asynchronously log a debug message.

        The message should be a format string
        (e.g., "Debugging {function}"),
        and keyword arguments will be used to fill in the placeholders.
        """
        ...
