import datetime

from app.domain.entities.user import User


class FakePasswordService:
    """Fake implementation of PasswordService for testing."""

    def hash_password(self, password: str) -> str:
        return f"hashed_{password}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        return password_hash == f"hashed_{password}"


def test_user_entity_set_password():
    user = User(email="test@example.com")
    pw_service = FakePasswordService()
    user.set_password("password123", pw_service)
    assert user.password_hash == "hashed_password123"


def test_user_entity_verify_password():
    user = User(email="test@example.com")
    pw_service = FakePasswordService()
    user.set_password("password123", pw_service)
    assert user.verify_password("password123", pw_service) is True
    assert user.verify_password("wrongpassword", pw_service) is False


def test_user_entity_to_dict():
    user = User(email="test@example.com")
    user.id = 1
    user.created_at = datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc)
    user.updated_at = None
    user.deleted_at = None

    expected = {
        "id": 1,
        "email": "test@example.com",
        "is_active": True,
        "is_admin": False,
        "created_at": "2023-01-01T00:00:00+00:00",
        "updated_at": None,
        "deleted_at": None,
    }

    assert user.to_dict() == expected
