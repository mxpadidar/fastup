import pytest
import sqlalchemy
import sqlalchemy.exc
from sqlalchemy import insert
from sqlalchemy.ext.asyncio.session import AsyncSession

from fastup.adapters.database.tbls import users_tbl


@pytest.fixture
def base_user_values() -> dict:
    return {
        "display_name": "Test User",
        "pwdhash": "hashed",
        "sex": "male",
        "status": "active",
        "is_admin": False,
    }


async def test_users_tbl_insert_success_with_just_email(
    async_session: AsyncSession, base_user_values: dict
):
    stmt = insert(users_tbl).values(
        {**base_user_values, "email": "a@example.com", "phone": None}
    )
    try:
        await async_session.execute(stmt)
        await async_session.commit()
    finally:
        await async_session.execute(
            users_tbl.delete().where(users_tbl.c.email == "a@example.com")
        )
        await async_session.commit()


async def test_users_tbl_insert_success_with_just_phone(
    async_session: AsyncSession,
    base_user_values: dict,
):
    stmt = insert(users_tbl).values(
        {**base_user_values, "email": None, "phone": "+15551234567"}
    )
    try:
        await async_session.execute(stmt)
        await async_session.commit()
    finally:
        await async_session.execute(
            users_tbl.delete().where(users_tbl.c.phone == "+15551234567")
        )
        await async_session.commit()


async def test_users_tbl_insert_fails_without_email_and_phone(
    async_session: AsyncSession,
    base_user_values: dict,
):
    stmt = insert(users_tbl).values({**base_user_values, "email": None, "phone": None})

    with pytest.raises(sqlalchemy.exc.IntegrityError) as exc_info:
        await async_session.execute(stmt)
        await async_session.commit()

    assert "ck_users_email_or_phone_not_null" in str(exc_info.value)
    await async_session.rollback()
