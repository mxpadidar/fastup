import dataclasses
import datetime

from fastup.core import enums

from .base_entity import Entity


@dataclasses.dataclass(kw_only=True)
class Otp(Entity):
    """Represents a single-use code used to prove control of an identity or to
    authorize a short-lived operation (signup, reset password, ...).
    """

    id: int
    phone: str
    intent: enums.OtpIntent
    status: enums.OtpStatus = enums.OtpStatus.ISSUED
    otp_hash: str
    attempts: int = 0
    ipaddr: str
    metadata: dict = dataclasses.field(default_factory=dict)
    created_at: datetime.datetime = dataclasses.field(init=False)
    expires_at: datetime.datetime
    consumed_at: datetime.datetime | None = None

    @property
    def is_expired(self) -> bool:
        """Check if the OTP has expired based on the current time."""
        return datetime.datetime.now(datetime.UTC) >= self.expires_at
