from app.adapters import db_registry
from app.domain.entities.user import User

from .tbls import users_tbl


def start_orm_mappings() -> None:
    """Initialize SQLAlchemy ORM mappings for domain entities.

    Maps domain entity classes to their corresponding database tables
    using imperative mapping. This allows domain entities to remain
    framework-agnostic while being persisted via SQLAlchemy.

    Must be called before any database operations.
    """
    db_registry.map_imperatively(User, users_tbl)
