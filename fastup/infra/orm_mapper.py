import logging

from fastup.core import entities

from .db import mapper_registry
from .tables import users

logger = logging.getLogger(__name__)


def start_orm_mapper() -> None:  # pragma: no cover
    """Initialize SQLAlchemy ORM mappings for domain entities.

    Maps domain entity classes to their corresponding database tables
    using imperative mapping. This allows domain entities to remain
    framework-agnostic while being persisted via SQLAlchemy.

    Must be called before any database operations.
    """
    logger.info("Starting Orm...")

    mapper_registry.map_imperatively(entities.User, users)
