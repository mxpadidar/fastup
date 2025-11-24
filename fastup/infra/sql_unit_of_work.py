import typing

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from fastup.core import exceptions
from fastup.core.unit_of_work import UnitOfWork
from fastup.infra import db, sql_repositories


class SQLUnitOfwWork(UnitOfWork):
    """SQLAlchemy implementation of UnitOfWork for managing database transactions."""

    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession] = db.sessionmaker
    ) -> None:
        """Initialize the UoW with a session factory.

        :param session_factory: Factory to create AsyncSession instances.
        """
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> typing.Self:
        """Enter the async context: create a new session and initialize repositories."""
        session = self._session_factory()
        self._session = session
        self.users = sql_repositories.UserSQLRepo(session)
        self.otps = sql_repositories.OtpSQLRepo(session)
        await super().__aenter__()
        return self

    async def __aexit__(self, *args) -> None:
        """Exit the async context: rollback on error and close the session."""
        if self._session:
            await self._session.close()
        await super().__aexit__(*args)

    @property
    def is_ready(self) -> bool:
        """Check if the repository has an active database session."""
        return self._session is not None

    @property
    def session(self) -> AsyncSession:
        """Get the current session."""
        if self._session is None:
            raise exceptions.UnitOfWorkContextExc
        return self._session

    async def _commit(self) -> None:
        """Commit the current transaction."""
        await self.session.commit()

    async def _rollback(self) -> None:
        """Rollback the current transaction."""
        if self._session:
            await self._session.rollback()
            self._session = None
