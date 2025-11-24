import dataclasses


@dataclasses.dataclass(frozen=True)
class Command:
    """Base class for all domain commands."""

    pass


@dataclasses.dataclass(frozen=True)
class IssueSignupOtpCommand(Command):
    phone: str
    ipaddr: str
