import asyncio
import logging
from typing import Any

from fastup.domain.logger import Logger


class BuiltInLogger(Logger):
    """built-in implementation of the logger interface"""

    def __init__(self, name: str, **kwargs) -> None:
        """initialize the logger with a name and configuration path."""
        super().__init__(name, **kwargs)
        self._logger = logging.getLogger(name)

    async def info(self, message: str, **kwargs: Any) -> None:
        await self._log(self._logger.info, message, **kwargs)

    async def error(self, message: str, **kwargs: Any) -> None:
        await self._log(self._logger.error, message, **kwargs)

    async def debug(self, message: str, **kwargs: Any) -> None:
        await self._log(self._logger.debug, message, **kwargs)

    async def _log(self, log_method, message: str, **kwargs: Any) -> None:
        try:
            formatted = message.format(**kwargs)
        except KeyError as e:
            formatted = f"[logger formatting error: missing key {e}] {message}"
        await asyncio.to_thread(log_method, formatted)
