import sqlalchemy as sa

from app.adapters import db_registry

users_tbl = sa.Table(
    "users",
    db_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String, nullable=False, unique=True),
    sa.Column("password_hash", sa.String, nullable=False),
    sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
    sa.Column("is_admin", sa.Boolean, nullable=False, server_default=sa.false()),
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
    sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
)
