import typing

from fastup.core import enums


class Publisher(typing.Protocol):
    """Protocol defining the interface for publishing external events."""

    async def publish(self, type: enums.EventType, payload: dict) -> None:
        """Publish a message to a specific delivery channel.

        :param type: The type of event being published.
        :param payload: The message payload to be sent.
        """
        ...
