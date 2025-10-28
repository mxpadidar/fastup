from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.entities import User
from app.domain.errors import ConflictErr
from app.domain.handlers import handle_create_user
from app.domain.protocols import PasswordService


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)
    uow.users = MagicMock()
    uow.users.get_by_email = AsyncMock()
    uow.users.add = AsyncMock()
    uow.users.refresh = AsyncMock()
    uow.commit = AsyncMock()
    return uow


@pytest.fixture
def mock_pw_service():
    service = MagicMock(spec=PasswordService)
    service.hash_password = MagicMock(return_value="hashed_password")
    return service


async def test_handle_create_user_valid_data(
    mock_uow: MagicMock, mock_pw_service: MagicMock
):
    mock_uow.users.get_by_email.return_value = None
    email = "test@example.com"
    password = "secure_password"

    user = await handle_create_user(
        mock_uow, mock_pw_service, email=email, password=password
    )

    assert isinstance(user, User)
    assert user.email == email
    assert user.is_active is False


async def test_handle_create_user_existing_email_raise_conflict(
    mock_uow: MagicMock, mock_pw_service: MagicMock
):
    existing_user = User(email="test@example.com", is_active=False)
    mock_uow.users.get_by_email.return_value = existing_user
    email = "test@example.com"
    password = "secure_password"

    with pytest.raises(ConflictErr):
        await handle_create_user(
            mock_uow, mock_pw_service, email=email, password=password
        )
