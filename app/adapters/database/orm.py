import datetime

import sqlalchemy as sa

from app.domain.entities import User

from .database import mapper_registry

users_table = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String, unique=True, nullable=False),
    sa.Column("created_at", sa.DateTime, default=datetime.datetime.now),
)


def start_mappers() -> None:  # pragma: no cover
    """Map entities to the database tables."""
    mapper_registry.map_imperatively(User, users_table)
