import sqlalchemy as sa
from sqlalchemy.orm import registry

from fastup.domain.entities import User

mapper_registry = registry()


users_table = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String, unique=True, nullable=False),
)


def start_mappers() -> None:
    """map entities to the database tables."""
    mapper_registry.map_imperatively(User, users_table)
