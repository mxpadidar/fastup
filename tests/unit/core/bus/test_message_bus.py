import asyncio
import dataclasses
from unittest.mock import AsyncMock

import pytest

from fastup.core.bus import MessageBus
from fastup.core.commands import Command
from fastup.core.entities import Entity
from fastup.core.events import Event


@dataclasses.dataclass(frozen=True)
class Cmd(Command):
    aggr_name: str


@dataclasses.dataclass(frozen=True)
class Ev(Event):
    aggr_id: int


@dataclasses.dataclass(kw_only=True)
class Aggregate(Entity):
    id: int
    name: str
    handled: bool = False


async def test_handle_puts_events_in_queue_and_dispatch_processes_them():
    """Ensure command handlers enqueue events and the dispatcher invokes the event handlers."""
    aggregates: dict[int, Aggregate] = {}
    queue = asyncio.Queue()

    async def create_aggregate_handler(
        cmd: Cmd, queue: asyncio.Queue = queue
    ) -> Aggregate:
        agg = Aggregate(id=1, name=cmd.aggr_name, handled=False)
        aggregates[agg.id] = agg
        queue.put_nowait(Ev(aggr_id=agg.id))
        return agg

    async def mark_aggregate(ev: Ev) -> None:
        aggregates[ev.aggr_id].handled = True

    bus = MessageBus(
        command_handlers={Cmd: create_aggregate_handler},
        event_handlers={Ev: [mark_aggregate]},
        queue=queue,
    )

    result: Aggregate = await bus.handle(Cmd(aggr_name="sample"))  # type: ignore
    await bus._dispatch_events()

    assert result.handled is True
    assert aggregates[result.id].handled is True


async def test_handle_raises_error_for_missing_command_handler():
    """Verify that handling a command with no registered handler raises RuntimeError."""
    bus = MessageBus(command_handlers={}, event_handlers={}, queue=asyncio.Queue())
    with pytest.raises(RuntimeError):
        await bus.handle(Cmd(aggr_name="x"))


async def test_dispatch_events_calls_all_event_handlers():
    """Verify that all handlers registered for an event type are invoked."""
    invoked: list[str] = []

    async def handler_a(ev: Ev):
        await asyncio.sleep(0.01)
        invoked.append("a")

    async def handler_b(ev: Ev):
        await asyncio.sleep(0.01)
        invoked.append("b")

    bus = MessageBus(
        command_handlers={},
        event_handlers={Ev: [handler_a, handler_b]},
        queue=asyncio.Queue(),
    )

    await bus.queue.put(Ev(aggr_id=1))
    await bus._dispatch_events()

    assert set(invoked) == {"a", "b"}


async def test_dispatch_events_does_not_propagate_handler_exceptions():
    """Ensure handler exceptions are swallowed instead of propagated."""
    failing_handler = AsyncMock(side_effect=RuntimeError("fail"))

    bus = MessageBus(
        command_handlers={},
        event_handlers={Ev: [failing_handler]},
        queue=asyncio.Queue(),
    )

    await bus.queue.put(Ev(aggr_id=1))

    # should NOT raise
    await bus._dispatch_events()


async def test_dispatch_noop_when_event_has_no_registered_handlers():
    """Ensure dispatch completes quietly when no handlers are registered."""
    bus = MessageBus(command_handlers={}, event_handlers={}, queue=asyncio.Queue())

    await bus.queue.put(Ev(aggr_id=99))

    # should simply exit without error
    await bus._dispatch_events()


async def test_dispatch_events_skips_non_event_items():
    """Ensure the dispatcher ignores items in the queue that are not Event instances."""
    bus = MessageBus(command_handlers={}, event_handlers={}, queue=asyncio.Queue())

    # put invalid item
    await bus.queue.put("not-an-event")  # type: ignore

    # should not raise, just skip it
    await bus._dispatch_events()
