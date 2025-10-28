import logging
import typing

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import errors
from app.domain.base import UnitOfWork

from .sqlalchemy_repos import UserSQLAlchemyRepo

logger = logging.getLogger(__name__)


class SqlAlchemyUoW(UnitOfWork):
    """SQLAlchemy implementation of UnitOfWork for managing database transactions."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        """Initialize the UoW with a session factory.

        :param session_factory: Factory to create AsyncSession instances.
        """
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> typing.Self:
        """Enter the async context: create a new session and initialize repositories."""
        session = self._session_factory()
        self._session = session
        self.users = UserSQLAlchemyRepo(session)
        await super().__aenter__()
        return self

    async def __aexit__(self, *args) -> None:
        """Exit the async context: rollback on error and close the session."""
        if self._session:
            await self._session.close()
        await super().__aexit__(*args)

    @property
    def is_ready(self) -> bool:
        return self._session is not None

    async def _commit(self) -> None:
        """Commit the current transaction."""
        await self.session.commit()

    async def _rollback(self) -> None:
        """Rollback the current transaction."""
        if self._session:
            await self._session.rollback()
            self._session = None

    @property
    def session(self) -> AsyncSession:
        """Get the current session."""
        if self._session is None:
            logger.error("UnitOfWork is not ready")
            raise errors.UoWIsNotReady
        return self._session
