import dataclasses

from fastup.core.events import Event


@dataclasses.dataclass
class Entity:
    """Base class for all domain entities."""

    _events: set[Event] = dataclasses.field(default_factory=set, repr=False)

    @property
    def events(self) -> set[Event]:  # pragma: no cover
        """Returns the set of recorded events for the entity."""
        if not hasattr(self, "_events"):
            self._events = set()
        return self._events

    @events.setter
    def events(self, value: set[Event]) -> None:  # pragma: no cover
        """Sets the recorded events for the entity."""
        self._events = value

    def record_event(self, event: Event) -> None:  # pragma: no cover
        """Records a single event to be dispatched later.

        :param event: The domain event that has occurred.
        """
        self.events.add(event)

    def clear_events(self) -> None:  # pragma: no cover
        """Clears all recorded events from the entity."""
        self.events.clear()
