from typing import Self

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database:
    _instance: Self | None = None
    _initialized: bool = False

    def __new__(cls, *args, **kwargs) -> Self:
        print("-----------------------------------------")
        if cls._instance is not None:
            raise RuntimeError("database instance already initialized.")
        return super().__new__(cls)

    def __init__(
        self,
        url: str,
        pool_size: int = 5,
        pool_timeout: float = 30.0,
        max_overflow: int = 10,
        echo: bool = False,
    ) -> None:
        if self._initialized:
            print("database instance already initialized")
            raise RuntimeError
        else:
            print("initializing database instance...")

        self._url = url
        self._pool_size = pool_size
        self._pool_timeout = pool_timeout
        self._max_overflow = max_overflow
        self._echo = echo

        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None
        self._initialized = True

    @property
    def url(self) -> str:
        return self._url

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(
                self._url,
                pool_size=self._pool_size,
                pool_timeout=self._pool_timeout,
                max_overflow=self._max_overflow,
                echo=self._echo,
                future=True,
            )
        return self._engine

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        if self._sessionmaker is None:
            self._sessionmaker = async_sessionmaker(
                bind=self.engine, expire_on_commit=False
            )
        return self._sessionmaker

    async def close(self) -> None:
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
        self._sessionmaker = None
        self._initialized = False
        self._instance = None
