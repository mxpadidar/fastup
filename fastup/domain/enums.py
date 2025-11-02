import enum


class UserSex(enum.StrEnum):
    MALE = enum.auto()
    FEMALE = enum.auto()
    OTHER = enum.auto()


class UserStatus(enum.StrEnum):
    ACTIVE = enum.auto()
    INACTIVE = enum.auto()
    BANNED = enum.auto()
