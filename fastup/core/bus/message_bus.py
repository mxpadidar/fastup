import asyncio
import logging

from fastup.core.commands import Command
from fastup.core.entities import Entity
from fastup.core.events import Event

from .registry import Handler

logger = logging.getLogger(__name__)


class MessageBus:
    """Message bus coordinating command dispatch and domain-event dispatch."""

    def __init__(
        self,
        command_handlers: dict[type[Command], Handler],
        event_handlers: dict[type[Event], list[Handler]],
        queue: asyncio.Queue[Event],
    ) -> None:
        """Initialize the message bus with command and event handlers.

        :param command_handlers: mapping Command class -> async callable
        :param event_handlers: mapping Event class -> set of async callables
        :param queue: An asyncio queue for managing internal events.
        """
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers
        self.queue = queue

    async def handle(self, command: Command) -> Entity:
        """Handle a command by dispatching it to the appropriate handler.

        Executes the command handler, collects any events raised by the resulting entity,
        dispatches those events, and clears the entity's event queue.

        :param command: The command instance to handle.
        :return: The entity resulting from handling the command.
        :raises HandlerNotRegistered: If no handler is registered for the command type.
        """
        handler = self.command_handlers.get(command.type)

        if handler is None:
            raise RuntimeError(f"No handler registered for {command.name=}")

        logger.debug(f"handling {command.name=}")
        entity = await handler(command)
        await self._dispatch_events()
        return entity

    async def _dispatch_events(self) -> None:
        """Process all pending events in the queue.

        Pulls events from the internal queue until it's empty and invokes
        all registered handlers for each event."""
        while True:
            try:
                event = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                break

            if not isinstance(event, Event):
                logger.warning(f"Invalid event in queue: {event}")
                continue

            handlers = self.event_handlers.get(event.type, [])
            if not handlers:
                logger.warning(f"No handler registered for {event.name=}")
                continue

            logger.debug(f"dispatching {event.name=}")

            for handler in handlers:
                try:
                    await handler(event)
                    logger.debug(f"handled {event.name=} with {handler.__name__}")
                except Exception as exc:
                    logger.error(f"Error handling event {event.name=}: {exc}")
