import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from fastup.domain.entities.user import User


async def test_orm_user_mapping(async_session: AsyncSession) -> None:
    # Create and add a user
    new_user = User()
    new_user.email = "test@example.com"

    async_session.add(new_user)
    await async_session.commit()

    # Query the user back
    stmt = sa.select(User).where(User.email == "test@example.com")  # type: ignore
    result = await async_session.execute(stmt)
    user_record = result.scalar_one()

    # Assert that the user record is an instance of User and has the correct email
    assert isinstance(user_record, User)
    assert user_record.email == "test@example.com"

    # Clean up the session
    await async_session.delete(user_record)
    await async_session.commit()
