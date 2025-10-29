import typing

import httpx
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app import adapters
from app.adapters import sqlalchemy_repos
from app.domain import base, entities, protocols, repositories
from app.entrypoint import deps
from app.main import app

db_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
db_sessionmaker = async_sessionmaker(db_engine, expire_on_commit=False)

app.dependency_overrides[deps.get_uow] = lambda: adapters.SqlAlchemyUoW(db_sessionmaker)


@pytest.fixture
async def async_client() -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
def password_service() -> protocols.PasswordService:
    return adapters.PwdlibPasswordService()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database() -> typing.AsyncGenerator[None, None]:
    async with db_engine.begin() as conn:
        await conn.run_sync(adapters.db_registry.metadata.create_all)
    adapters.start_orm_mappings()
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(adapters.db_registry.metadata.drop_all)
    await db_engine.dispose()


@pytest.fixture
async def db_session() -> typing.AsyncGenerator[AsyncSession, None]:
    """Provide a per-test AsyncSession."""
    async with db_sessionmaker() as session:
        yield session


@pytest.fixture
def user_factory(
    password_service: protocols.PasswordService,
) -> typing.Callable[[int, str], entities.User]:
    def factory(id: int, email: str) -> entities.User:
        user = entities.User(email=email)
        user.id = id
        user.set_password("password", password_service)
        return user

    return factory


@pytest.fixture
async def user(
    user_factory: typing.Callable[[int, str], entities.User], db_session: AsyncSession
) -> typing.AsyncGenerator[entities.User, None]:
    user = user_factory(100000, "test@example.com")
    db_session.add(user)
    await db_session.commit()
    yield user
    await db_session.delete(user)
    await db_session.commit()


@pytest.fixture
def user_repo(db_session: AsyncSession) -> repositories.UserRepo:
    return sqlalchemy_repos.UserSQLAlchemyRepo(db_session)


@pytest.fixture
async def uow() -> typing.AsyncGenerator[base.UnitOfWork, None]:
    yield adapters.SqlAlchemyUoW(db_sessionmaker)


@pytest.fixture(scope="session")
def token_service() -> protocols.TokenService:
    return adapters.JwtTokenService(
        secret_key="secret", issuer="testiss", audience="testaud"
    )
