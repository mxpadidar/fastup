import asyncio
import logging
import typing

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
    ) -> None:
        """Initialize the message bus with command and event handlers.

        :param command_handlers: mapping Command class -> async callable
        :param event_handlers: mapping Event class -> set of async callables
        """
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers

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
        events = entity.events
        if events:
            await self.dispatch_events(events)
            entity.events.clear()

        return entity

    async def dispatch_events(self, events: set[Event]) -> None:
        """Dispatch a set of events to their registered handlers concurrently.

        For each event, finds the corresponding handlers and schedules them to run
        asynchronously. If no handlers are found for an event, logs a warning.

        :param events: Set of event instances to dispatch.
        """
        tasks: list[typing.Awaitable[None]] = []

        for ev in events:
            handlers = self.event_handlers.get(ev.type)
            if not handlers:
                logging.warning(f"No handler rgistered for {ev.name=}")
                continue
            tasks.extend([h(ev) for h in handlers])

        if not tasks:
            return

        await asyncio.gather(*tasks)
