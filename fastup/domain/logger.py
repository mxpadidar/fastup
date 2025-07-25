# pragma: no cover
from abc import ABC, abstractmethod
from typing import Callable

type LoggerFactory = Callable[[str], "Logger"]


class Logger(ABC):
    """abstract base class for structured, asynchronous logging."""

    def __init__(self, name: str, **kwargs) -> None:
        """initialize the logger with a name and configuration path."""
        self.name = name
        self.configs = kwargs

    @abstractmethod
    async def info(self, message: str, **kwargs) -> None:
        """asynchronously log an informational message."""
        ...

    @abstractmethod
    async def error(self, message: str, **kwargs) -> None:
        """asynchronously log an error message."""
        ...

    @abstractmethod
    async def debug(self, message: str, **kwargs) -> None:
        """asynchronously log a debug message."""
        ...
