import dataclasses

import pytest

from fastup.core import exceptions
from fastup.core.entities import Entity
from fastup.core.repositories import Repository


@dataclasses.dataclass
class MockEntity(Entity):
    id: int


class FakeRepo(Repository[MockEntity]):
    """A fake repository implementation for testing the base class logic."""

    def __init__(self, entities: list[MockEntity] | None = None):
        self._items = {e.id: e for e in entities} if entities else {}

    async def _get(self, **kwargs) -> MockEntity | None:
        # A simple implementation that only supports filtering by id
        id_val = kwargs.get("id")
        if id_val is None:
            # Simulate an invalid filter argument
            raise ValueError("FakeRepo only supports filtering by 'id'.")
        return self._items.get(id_val)

    async def add(self, entity: MockEntity) -> None:
        self._items[entity.id] = entity
        print(f"Added entity {entity.id}")

    async def delete(self, entity: MockEntity) -> None:
        if entity.id in self._items:
            del self._items[entity.id]
            print(f"Deleted entity {entity.id}")

    async def refresh(self, entity: MockEntity) -> None:
        # No-op for this fake implementation
        print(f"Refreshed entity {entity.id}")


@pytest.fixture
def repo() -> FakeRepo:
    # Pre-populate the repo with one entity for consistent testing
    return FakeRepo(entities=[MockEntity(id=1)])


# 3. Updated tests that match the new Repository behavior
async def test_repo_get_raises_exc_when_called_without_filters(repo: FakeRepo):
    """Verifies that get() raises InternalExc if no filter arguments are provided."""
    with pytest.raises(
        exceptions.InternalExc, match="get must be called with at least one filter"
    ):
        await repo.get()


async def test_repo_get_returns_none_for_nonexistent_id(repo: FakeRepo):
    """Verifies that get() returns None when no entity matches the filter."""
    result = await repo.get(id=999)
    assert result is None


async def test_repo_get_propagates_exceptions_from_implementation(repo: FakeRepo):
    """Verifies that get() propagates exceptions (e.g., ValueError) from _get()."""
    with pytest.raises(ValueError, match="FakeRepo only supports filtering by 'id'"):
        # Use a filter that the FakeRepo's _get implementation doesn't support
        await repo.get(name="invalid_filter")


async def test_repo_get_returns_entity_for_existing_id(repo: FakeRepo):
    """Verifies that get() returns the correct entity when a match is found."""
    result = await repo.get(id=1)
    assert isinstance(result, MockEntity)
    assert result.id == 1


async def test_repo_get_or_raise_raises_notfoundexc_for_nonexistent_id(repo: FakeRepo):
    """Verifies that get_or_raise() raises NotFoundExc for a non-matching filter."""
    with pytest.raises(
        exceptions.NotFoundExc, match="The requested entity was not found"
    ):
        await repo.get_or_raise(id=999)


async def test_repo_get_or_raise_returns_entity_for_existing_id(repo: FakeRepo):
    """Verifies that get_or_raise() returns the entity when a match is found."""
    result = await repo.get_or_raise(id=1)
    assert isinstance(result, MockEntity)
    assert result.id == 1
