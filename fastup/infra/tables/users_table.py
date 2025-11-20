import sqlalchemy as sa

from fastup.infra.db import mapper_registry

users = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("email", sa.String, nullable=False, unique=True),
    sa.Column("pwdhash", sa.String, nullable=False),
    sa.Column("fname", sa.String, nullable=True),
    sa.Column("lname", sa.String, nullable=True),
    sa.Column("sex", sa.String, nullable=False),
    sa.Column("status", sa.String, nullable=False, index=True),
    sa.Column("is_admin", sa.Boolean, nullable=False),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
        index=True,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    ),
    sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True, index=True),
)
