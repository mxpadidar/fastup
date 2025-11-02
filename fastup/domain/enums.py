import enum


class UserSex(enum.StrEnum):
    MALE = enum.auto()
    FEMALE = enum.auto()
    OTHER = enum.auto()


class UserStatus(enum.StrEnum):
    INCOMPLETE = enum.auto()
    ACTIVE = enum.auto()
    BANNED = enum.auto()


class AuthMethod(enum.StrEnum):
    EMAIL = enum.auto()
    PHONE = enum.auto()


class AuthIntent(enum.StrEnum):
    REGISTER = enum.auto()
    CHANGE_PWD = enum.auto()
    RESET_PW = enum.auto()


class SessionStatus(enum.StrEnum):
    PENDING = enum.auto()
    ACTIVE = enum.auto()
    REVOKED = enum.auto()
    EXPIRED = enum.auto()
