import dataclasses

from fastup.core import enums


@dataclasses.dataclass(frozen=True)
class Command:
    """Base class for all domain commands."""

    @property
    def type(self) -> type["Command"]:  # pragma: no cover
        return type(self)

    @property
    def name(self) -> str:  # pragma: no cover
        return self.__class__.__name__


@dataclasses.dataclass(frozen=True)
class IssueSignupOtpCommand(Command):
    phone: str
    ipaddr: str


@dataclasses.dataclass(frozen=True)
class VerifyOtpCommand(Command):
    otp_id: int
    code: str
    ipaddr: str


@dataclasses.dataclass(frozen=True)
class SignupCommand(Command):
    otp_id: int
    ipaddr: str
    password: str
    sex: enums.UserSex
    first_name: str | None
    last_name: str | None
