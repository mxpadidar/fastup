import sqlalchemy as sa

from fastup.infra.db import mapper_registry

otps = sa.Table(
    "otps",
    mapper_registry.metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=False),
    sa.Column("phone", sa.String, nullable=False, index=True),
    sa.Column("intent", sa.String, nullable=False, index=True),
    sa.Column("status", sa.String, nullable=False, index=True),
    sa.Column("otp_hash", sa.String, nullable=False),
    sa.Column("attempts", sa.Integer, nullable=False, server_default="0"),
    sa.Column("ipaddr", sa.String, nullable=False),
    sa.Column("metadata", sa.JSON, nullable=False, server_default=sa.text("'{}'")),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False, index=True),
    sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True, index=True),
)
