from typing import Callable

from fastup.core.commands import Command
from fastup.core.events import Event

type Handler[T, **P] = Callable[P, T]

EVENT_HANDLERS: dict[type["Event"], list[Handler]] = {}

COMMAND_HANDLERS: dict[type[Command], Handler] = {}


def register_command[T, **P](cmd: type[Command]) -> Callable[[Handler], Handler]:
    """Register a function as the handler for the given Command type."""

    def innder(func: Handler) -> Handler:
        if cmd in COMMAND_HANDLERS:
            raise RuntimeError
        COMMAND_HANDLERS[cmd] = func
        return func

    return innder


def register_event[T, **P](ev: type[Event]) -> Callable[[Handler], Handler]:
    """Register a function as an event handler for the given Event type."""

    def decorator(func: Handler) -> Handler:
        EVENT_HANDLERS.setdefault(ev, []).append(func)
        return func

    return decorator
