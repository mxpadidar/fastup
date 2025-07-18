import asyncio
import logging

from fastup.domain.core.logger import Logger


class BuiltInLogger(Logger):
    """Concrete implementation of the Logger interface using Python's built-in
    logging module. Supports asynchronous logging by running logging
    operations in a background thread."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="[{asctime}] [{levelname}] {name} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    async def info(self, message: str, **kwargs) -> None:
        await self._log(self._logger.info, message, **kwargs)

    async def error(self, message: str, **kwargs) -> None:
        await self._log(self._logger.error, message, **kwargs)

    async def debug(self, message: str, **kwargs) -> None:
        await self._log(self._logger.debug, message, **kwargs)

    async def _log(self, log_method, message: str, **kwargs) -> None:
        formatted = message.format(**kwargs) if kwargs else message
        await asyncio.to_thread(log_method, formatted)
