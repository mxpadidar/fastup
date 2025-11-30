import asyncio
from unittest.mock import patch

import pytest

from fastup.core.bus import register_command, register_event
from fastup.core.commands import Command
from fastup.core.entities import Entity
from fastup.core.events import Event


class Cmd1(Command): ...


class Cmd2(Command): ...


class Ntt(Entity): ...


class Ev1(Event): ...


class Ev2(Event): ...


@patch("fastup.core.bus.registry.COMMAND_HANDLERS", new_callable=dict)
async def test_register_command_adds_handler(command_handlers_mock: dict):
    """A command handler should be registered exactly for its command."""

    @register_command(Cmd1)
    async def handler(cmd: Cmd1) -> Entity:
        return Ntt()

    assert command_handlers_mock[Cmd1] is handler


@patch("fastup.core.bus.registry.COMMAND_HANDLERS", new_callable=dict)
async def test_register_command_rejects_duplicates(command_handlers_mock: dict):
    """Registering a second handler for the same command must raise."""

    @register_command(Cmd1)
    async def h1(cmd: Cmd1) -> Entity: ...

    with pytest.raises(RuntimeError):

        @register_command(Cmd1)
        async def h2(cmd: Cmd1) -> Entity: ...


@patch("fastup.core.bus.registry.COMMAND_HANDLERS", new_callable=dict)
async def test_registered_command_handler_is_async_callable(
    command_handlers_mock: dict,
):
    """Registered command handlers must stay async callables."""

    @register_command(Cmd1)
    async def handler(cmd: Cmd1) -> Entity:
        return Ntt()

    registered = command_handlers_mock[Cmd1]
    assert asyncio.iscoroutinefunction(registered)
    result = await registered(Cmd1())
    assert isinstance(result, Ntt)


@patch("fastup.core.bus.registry.COMMAND_HANDLERS", new_callable=dict)
async def test_register_command_handlers_for_multiple_commands(
    command_handlers_mock: dict,
):
    """Different commands should not conflict."""

    @register_command(Cmd1)
    async def h1(cmd: Cmd1) -> Entity: ...

    @register_command(Cmd2)
    async def h2(cmd: Cmd2) -> Entity: ...

    assert command_handlers_mock[Cmd1] is h1
    assert command_handlers_mock[Cmd2] is h2


@patch("fastup.core.bus.registry.EVENT_HANDLERS", new_callable=dict)
async def test_register_event_adds_handler(event_handlers_mock: dict):
    """Multiple event handlers should be registered for the same event."""

    @register_event(Ev1)
    async def h1(event: Ev1): ...

    @register_event(Ev1)
    async def h2(event: Ev1): ...

    assert event_handlers_mock[Ev1] == [h1, h2]


@patch("fastup.core.bus.registry.EVENT_HANDLERS", new_callable=dict)
async def test_event_handlers_do_not_conflict_between_events(event_handlers_mock: dict):
    """Different events keep separate handler lists."""

    @register_event(Ev1)
    async def h1(event: Ev1): ...

    @register_event(Ev2)
    async def h2(event: Ev2): ...

    assert event_handlers_mock[Ev1] == [h1]
    assert event_handlers_mock[Ev2] == [h2]


@patch("fastup.core.bus.registry.EVENT_HANDLERS", new_callable=dict)
async def test_registered_event_handler_is_async_callable(event_handlers_mock: dict):
    """Event handlers must remain asynchronous."""

    @register_event(Ev1)
    async def handler(event: Ev1): ...

    registered = event_handlers_mock[Ev1][0]
    assert asyncio.iscoroutinefunction(registered)
    assert await registered(Ev1()) is None
