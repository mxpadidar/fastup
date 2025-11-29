import datetime
import typing


class Config(typing.Protocol):
    """Defines the central configuration contract for the application's core domain.

    This protocol ensures the domain layer is decoupled from the concrete
    infrastructure-level config implementation (e.g., Pydantic BaseSettings).
    """

    otp_length: int
    otp_max_attempts: int
    otp_rate_limit_max_requests: int
    otp_lifetime: datetime.timedelta
    otp_rate_limit_window: datetime.timedelta
