import dataclasses

import pytest

from fastup.domain import exceptions
from fastup.domain.ports import AbstractRepo


@dataclasses.dataclass
class Ntt:
    id: int


class FakeRepo(AbstractRepo[Ntt]):
    async def _get(self, **kwargs) -> Ntt | None:
        id = kwargs.get("id")
        if id is None:
            raise ValueError
        if id != 1:
            return None
        return Ntt(id=1)

    async def _delete(self, entity: Ntt, soft: bool = False) -> None:
        print(f"Deleting entity {entity} with soft={soft}")
        if soft:
            raise AttributeError
        return

    async def refresh(self, entity: Ntt) -> Ntt:
        return entity

    async def add(self, entity: Ntt) -> Ntt:
        return entity


@pytest.fixture
def repo() -> FakeRepo:
    return FakeRepo()


async def test_repo_get_without_filters_returns_none(repo: FakeRepo):
    result = await repo.get()
    assert result is None


async def test_repo_get_with_nonexistent_id_returns_none(repo: FakeRepo):
    result = await repo.get(id=999)
    assert result is None


async def test_repo_get_returns_none_on_error(repo: FakeRepo):
    result = await repo.get(name="invalid")  # will raise ValueError in _get
    assert result is None


async def test_repo_get_with_existing_id_returns_entity(repo: FakeRepo):
    result = await repo.get(id=1)
    assert result is not None
    assert result.id == 1


async def test_repo_get_or_raise_not_found_raises_exception(repo: FakeRepo):
    with pytest.raises(exceptions.NotFoundExc):
        await repo.get_or_raise_not_found(id=999)


async def test_repo_get_or_raise_not_found_returns_entity(repo: FakeRepo):
    result = await repo.get_or_raise_not_found(id=1)
    assert result is not None
    assert result.id == 1


async def test_repo_hard_delete(repo: FakeRepo):
    entity = Ntt(id=1)
    await repo.delete(entity, soft=False)  # Should complete without error


async def test_repo_soft_delete_raises_without_deleted_at(repo: FakeRepo):
    entity = Ntt(id=1)
    with pytest.raises(exceptions.LogicalExc):
        await repo.delete(entity, soft=True)
