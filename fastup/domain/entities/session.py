import dataclasses
import datetime
import typing
import uuid

from fastup.domain import enums


@dataclasses.dataclass
class Session:
    """Represents an issued session token (device session)."""

    id: int = dataclasses.field(init=False)
    uuid: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    user_id: int
    method: enums.AuthMethod
    status: enums.SessionStatus = enums.SessionStatus.PENDING
    ticket_id: int | None = None
    ipaddr: str
    metadata: dict[str, typing.Any] = dataclasses.field(default_factory=dict)
    rotate_count: int = 0  # track number of rotations in current window.
    window_started_at: datetime.datetime = dataclasses.field(init=False)
    last_rotated_at: datetime.datetime | None = None
    locked_until: datetime.datetime | None = None  # when rate limit is exceeded
    created_at: datetime.datetime = dataclasses.field(init=False)
    expires_at: datetime.datetime
