import sqlalchemy as sa

from fastup.adapters.database import mapper_registry

users_tbl = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column(
        "id",
        sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
        primary_key=True,
        autoincrement=True,
    ),
    sa.Column("display_name", sa.String, nullable=False),
    sa.Column("email", sa.String, nullable=True),
    sa.Column("phone", sa.String, nullable=True),
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
    # either email or phone should be provided
    sa.CheckConstraint(
        "(email IS NOT NULL) OR (phone IS NOT NULL)",
        name="ck_users_email_or_phone_not_null",
    ),
    # unique email, and phone (only when not null)
    # uncomment after switching to postgresql
    # sa.UniqueConstraint(
    #     "email",
    #     postgresql_where=sa.text("email IS NOT NULL"),
    # ),
    # sa.UniqueConstraint(
    #     "phone",
    #     postgresql_where=sa.text("phone IS NOT NULL"),
    # ),
)
