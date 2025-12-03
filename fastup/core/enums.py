import enum


class UserSex(enum.StrEnum):
    MALE = enum.auto()
    FEMALE = enum.auto()
    OTHER = enum.auto()


class UserStatus(enum.StrEnum):
    ACTIVE = enum.auto()
    INACTIVE = enum.auto()
    BANNED = enum.auto()


class OtpIntent(enum.StrEnum):
    SIGN_UP = enum.auto()


class OtpStatus(enum.StrEnum):
    ISSUED = enum.auto()
    SENT = enum.auto()
    CONSUMED = enum.auto()


class EventType(enum.StrEnum):
    NOTIFICATION = enum.auto()  # Server-Sent Events
