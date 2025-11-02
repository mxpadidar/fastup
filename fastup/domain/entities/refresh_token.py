import dataclasses
import datetime
import uuid


@dataclasses.dataclass
class RefreshToken:
    """Represents a long-lived credential to refresh access or rehydrate a session."""

    id: int = dataclasses.field(init=False)
    user_id: int
    session_uuid: uuid.UUID
    token_hash: str
    created_at: datetime.datetime = dataclasses.field(init=False)
    expires_at: datetime.datetime
    revoked_at: datetime.datetime | None = None
