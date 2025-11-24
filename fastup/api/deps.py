import functools
from typing import Annotated

from fastapi.params import Depends

from fastup.config import Config, get_config
from fastup.core import services
from fastup.core.unit_of_work import UnitOfWork
from fastup.infra import db
from fastup.infra.hash_services import Argon2PasswordHasher, HMACHasher
from fastup.infra.snowflake_idgen import SnowflakeIDGenerator
from fastup.infra.sql_unit_of_work import SQLUnitOfwWork


async def get_uow() -> UnitOfWork:
    """Provide Unit of Work instance for database operations."""
    return SQLUnitOfwWork(session_factory=db.sessionmaker)


@functools.cache
def get_idgen(
    config: Annotated[Config, Depends(get_config)],
) -> services.IDGenerator:
    """Provide singleton Snowflake ID generator instance."""
    return SnowflakeIDGenerator(
        epoch=config.snowflake_epoch,
        node_id=config.snowflake_node_id,
        worker_id=config.snowflake_worker_id,
    )


@functools.cache
def get_hmac_hasher(
    config: Annotated[Config, Depends(get_config)],
) -> services.HashService:
    """Provide singleton HMAC hasher instance."""
    return HMACHasher(key=config.hmac_secret_key)


@functools.cache
def get_pwd_hasher() -> services.HashService:
    """Provide singleton Argon2 password hasher instance."""
    return Argon2PasswordHasher()
