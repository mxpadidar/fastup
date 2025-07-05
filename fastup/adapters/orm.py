import sqlalchemy as sa
from sqlalchemy.orm import registry

from fastup.core.logger import get_logger
from fastup.domain.entities.user import User

logger = get_logger("orm")

mapper_registry = registry()


account_users_table = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String, unique=True, nullable=False),
)


def start_mappers():
    logger.info("starting mappers")
    mapper_registry.map_imperatively(User, account_users_table)
