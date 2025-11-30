import asyncio
import dataclasses
from unittest.mock import AsyncMock

import pytest

from fastup.core.bus import MessageBus
from fastup.core.commands import Command
from fastup.core.entities import Entity
from fastup.core.events import Event


@dataclasses.dataclass(frozen=True)
class CreateTestCommand(Command):
    """Command used in tests to create a test aggregate."""

    aggr_name: str


@dataclasses.dataclass(frozen=True)
class CreatedEvent(Event):
    """Event emitted when a test aggregate is created."""

    aggr_id: int


@dataclasses.dataclass(kw_only=True)
class Aggregate(Entity):
    """Simple test aggregate that records events and a handled flag."""

    id: int
    name: str
    handled: bool = False


async def test_handle_dispatches_command_and_triggers_event_handlers_and_clears_event_queue():
    """End-to-end: command -> handler -> events dispatched -> events cleared."""
    aggregates: dict[int, Aggregate] = {}

    async def create_aggregate_handler(cmd: CreateTestCommand) -> Aggregate:
        """Create an aggregate and record a CreatedEvent."""
        agg = Aggregate(id=1, name=cmd.aggr_name)
        event = CreatedEvent(aggr_id=agg.id)
        agg.record_event(event)
        aggregates[agg.id] = agg
        return agg

    async def mark_aggregate_handled(ev: CreatedEvent) -> None:
        """Mark the referenced aggregate as handled."""
        agg = aggregates[ev.aggr_id]
        agg.handled = True
        aggregates[agg.id] = agg

    bus = MessageBus(
        command_handlers={CreateTestCommand: create_aggregate_handler},
        event_handlers={CreatedEvent: [mark_aggregate_handled]},
    )

    returned = await bus.handle(CreateTestCommand(aggr_name="sample"))

    assert isinstance(returned, Aggregate)
    assert returned.events == set()
    assert returned.handled is True
    assert aggregates[returned.id].handled is True


async def test_handle_raises_if_command_handler_not_registered():
    """Raise RuntimeError when command handler is not registered."""
    bus = MessageBus(command_handlers={}, event_handlers={})
    with pytest.raises(RuntimeError):
        await bus.handle(CreateTestCommand(aggr_name="missing"))


async def test_dispatch_events_invokes_all_registered_handlers_per_event_concurrently():
    """Invoke all handlers for an event concurrently."""
    invoked: list[str] = []

    async def handler_a(ev: CreatedEvent) -> None:
        await asyncio.sleep(0.01)
        invoked.append("a")

    async def handler_b(ev: CreatedEvent) -> None:
        await asyncio.sleep(0.01)
        invoked.append("b")

    bus = MessageBus(
        command_handlers={}, event_handlers={CreatedEvent: [handler_a, handler_b]}
    )

    await bus.dispatch_events({CreatedEvent(aggr_id=1)})

    assert set(invoked) == {"a", "b"}
    assert len(invoked) == 2


async def test_dispatch_events_propagates_exceptions_from_handlers():
    """Exceptions in handlers propagate to the caller by default."""

    failing_handler = AsyncMock(side_effect=RuntimeError)
    bus = MessageBus(
        command_handlers={}, event_handlers={CreatedEvent: [failing_handler]}
    )

    with pytest.raises(RuntimeError):
        await bus.dispatch_events({CreatedEvent(aggr_id=1)})


async def test_dispatch_events_is_noop_when_there_are_no_handlers():
    """Dispatching events without handlers is a no-op."""
    bus = MessageBus(command_handlers={}, event_handlers={})
    await bus.dispatch_events({CreatedEvent(aggr_id=1)})
