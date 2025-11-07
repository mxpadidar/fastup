import datetime

import pytest

from fastup.domain.entities import User
from fastup.domain.enums import UserSex
from fastup.domain.exceptions import NotFoundExc
from fastup.domain.repositories import UserRepo


class FakeUserRepo(UserRepo):
    def __init__(self, users: list[User]) -> None:
        self._users = users

    async def _get(self, **kwargs) -> User | None:
        id = kwargs.get("id")
        email = kwargs.get("email")
        phone = kwargs.get("phone")
        deleted_at = kwargs.get("deleted_at")

        for user in self._users:
            if id is not None and user.id == id:
                if deleted_at is None and user.deleted_at is not None:
                    return None
                return user
            if email is not None and user.email == email:
                if deleted_at is None and user.deleted_at is not None:
                    return None
                return user
            if phone is not None and user.phone == phone:
                if deleted_at is None and user.deleted_at is not None:
                    return None
                return user
        else:
            return None

    async def _delete(self, entity: User, soft: bool = False) -> None:
        if soft:
            raise AttributeError
        return

    async def refresh(self, entity: User) -> User:
        return entity

    async def add(self, entity: User) -> User:
        return entity


@pytest.fixture
def sample_user() -> User:
    user = User(
        email="test@example.com",
        phone="+12025550122",
        display_name="Test User",
        pwdhash="hashed_password",
        sex=UserSex.MALE,
    )
    user.id = 1
    return user


@pytest.fixture
def deleted_user() -> User:
    user = User(
        email="deleted@example.com",
        phone="+12025550123",
        display_name="Deleted User",
        pwdhash="hashed_password",
        sex=UserSex.MALE,
        deleted_at=datetime.datetime.now(),
    )
    user.id = 2
    return user


@pytest.fixture
def repo(sample_user: User, deleted_user: User) -> FakeUserRepo:
    return FakeUserRepo(users=[sample_user, deleted_user])


async def test_user_repo_get_by_email_returns_user(repo: UserRepo, sample_user: User):
    assert sample_user.email
    got = await repo.get_by_email_or_raise(sample_user.email)
    assert got is sample_user
    assert got.email == sample_user.email


async def test_user_repo_get_by_email_raises_when_not_found(repo: UserRepo):
    with pytest.raises(NotFoundExc):
        await repo.get_by_email_or_raise("nonexists@mail.com")


async def test_user_repo_get_by_email_raises_for_soft_deleted_user(
    repo: UserRepo, deleted_user: User
):
    assert deleted_user.email
    with pytest.raises(NotFoundExc):
        await repo.get_by_email_or_raise(deleted_user.email)


async def test_user_repo_get_by_id_returns_user(repo: UserRepo, sample_user: User):
    got = await repo.get_by_id_or_raise(sample_user.id)
    assert got is sample_user


async def test_user_repo_get_by_id_raises_when_not_found(
    repo: UserRepo,
):
    with pytest.raises(NotFoundExc):
        await repo.get_by_id_or_raise(0)


async def test_user_repo_get_by_phone_returns_user(
    repo: UserRepo,
    sample_user: User,
):
    assert sample_user.phone
    got = await repo.get_by_phone_or_raise(sample_user.phone)
    assert got is sample_user


async def test_user_repo_get_by_phone_raises_when_not_found(
    repo: UserRepo,
):
    with pytest.raises(NotFoundExc):
        await repo.get_by_phone_or_raise("+19999999999")
