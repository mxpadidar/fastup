import datetime
import typing

import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from fastup.adapters.concrete import BaseSQLRepo
from fastup.domain.ports import AbstractRepo

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

db_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase): ...


class Ntt(Base):
    __tablename__ = "ntt"
    __mapper_args__ = {"confirm_deleted_rows": False}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(), nullable=True
    )


class FakeRepo(BaseSQLRepo[Ntt], AbstractRepo[Ntt]):
    @property
    def ntt(self) -> type[Ntt]:
        return Ntt

    @property
    def session(self) -> AsyncSession:
        return self._session


@pytest.fixture(scope="module", autouse=True)
async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def repo() -> typing.AsyncGenerator[FakeRepo, None]:
    async with db_factory() as session:
        yield FakeRepo(session)
        await session.rollback()


@pytest.fixture
async def ntt() -> typing.AsyncGenerator[Ntt, None]:
    instance = Ntt(name="test-ntt")
    async with db_factory() as session:
        session.add(instance)
        await session.flush()
        await session.refresh(instance)
        yield instance
        await session.delete(instance)
        await session.commit()


async def test_sqlrepo_get_return_None_without_filters(repo: FakeRepo):
    result = await repo.get()  # no filters provided should raise
    assert result is None


async def test_sqlrepo_add(repo: FakeRepo):
    # arrange: create a new entity
    entity = Ntt(name="added")

    # act: add the entity via the repository
    await repo.add(entity)

    # assert: entity should be persisted after flush
    await repo.session.flush()
    got = await repo.session.get(Ntt, entity.id)
    assert got is not None
    assert got.id == entity.id


async def test_sqlrepo_get(ntt: Ntt, repo: FakeRepo):
    got = await repo.get(id=ntt.id)
    assert got is not None
    assert got.id == ntt.id


async def test_sqlrepo_get_nonexistent(repo: FakeRepo):
    got = await repo.get(id=0)
    assert got is None


async def test_sqlrepo_get_soft_deleted(repo: FakeRepo, ntt: Ntt):
    # arrange: soft-delete the entity directly via SQL
    await repo.session.execute(
        sqlalchemy.text("UPDATE ntt SET deleted_at = CURRENT_TIMESTAMP WHERE id = :id"),
        {"id": ntt.id},
    )
    # await session.commit()

    # act & assert: get should return None when filtering out soft-deleted
    got = await repo.get(id=ntt.id, deleted_at=None)
    assert got is None


async def test_sqlrepo_get_by_name(repo: FakeRepo, ntt: Ntt):
    got = await repo.get(name=ntt.name, deleted_at=None)
    assert got is not None
    assert got.id == ntt.id


async def test_sqlrepo_get_by_name_nonexistent(repo: FakeRepo):
    got = await repo.get(name="does-not-exist", deleted_at=None)
    assert got is None


async def test_sqlrepo_get_by_name_soft_deleted(repo: FakeRepo, ntt: Ntt):
    # arrange: soft-delete the entity directly via SQL
    await repo.session.execute(
        sqlalchemy.text("UPDATE ntt SET deleted_at = CURRENT_TIMESTAMP WHERE id = :id"),
        {"id": ntt.id},
    )
    await repo.session.commit()

    # act & assert: get should return None when filtering out soft-deleted
    got = await repo.get(name=ntt.name, deleted_at=None)
    assert got is None


async def test_sqlrepo_soft_delete(repo: FakeRepo, ntt: Ntt):
    # arrange: fetch a fresh, attached instance of the entity from the repo's session
    db_ntt = await repo.session.get(Ntt, ntt.id)
    assert db_ntt is not None

    # act: perform a soft delete through the repository
    await repo.delete(db_ntt, soft=True)

    # assert: the row should still exist but have deleted_at set
    deleted = await repo.session.get(Ntt, ntt.id)
    assert deleted is not None
    assert deleted.deleted_at is not None

    # act & assert: get should return None when filtering out soft-deleted
    got = await repo.session.execute(
        sqlalchemy.select(Ntt).where(Ntt.id == ntt.id, Ntt.deleted_at.is_(None))
    )
    assert got.scalar_one_or_none() is None


async def test_sqlrepo_hard_delete(repo: FakeRepo, ntt: Ntt):
    # arrange: fetch a fresh, attached instance of the entity from the repo's session
    row = await repo.session.execute(sqlalchemy.select(Ntt).where(Ntt.id == ntt.id))
    db_ntt = row.scalar_one()

    # act: perform a hard delete through the repository
    await repo.delete(db_ntt, soft=False)

    # assert: the row should no longer exist
    row = await repo.session.execute(sqlalchemy.select(Ntt).where(Ntt.id == db_ntt.id))
    assert row.scalar_one_or_none() is None


async def test_sqlrepo_refresh(repo: FakeRepo, ntt: Ntt):
    # arrange: fetch a fresh, attached instance of the entity from the repo's session
    db_ntt = await repo.session.get(Ntt, ntt.id)
    assert db_ntt is not None

    # arrange: modify the entity directly via SQL to simulate an external change
    original_name = ntt.name
    new_name = "modified"
    await repo.session.execute(
        sqlalchemy.text("UPDATE ntt SET name = :name WHERE id = :id"),
        {"name": new_name, "id": ntt.id},
    )

    # act: refresh the entity via the repository
    refreshed = await repo.refresh(db_ntt)

    # assert: the refreshed entity should reflect the updated name
    assert refreshed.name != original_name
    assert refreshed.name == new_name
    assert refreshed.id == ntt.id
