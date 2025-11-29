import dataclasses


@dataclasses.dataclass(frozen=True)
class Event:
    """Base class for all domain events."""

    @property
    def type(self) -> type["Event"]:  # pragma: no cover
        return type(self)

    @property
    def name(self) -> str:  # pragma: no cover
        return self.__class__.__name__


@dataclasses.dataclass(frozen=True)
class OtpIssuedEvent(Event):
    """Event fired when a OTP has been created and should be delivered."""

    otp_id: int
    code: str
