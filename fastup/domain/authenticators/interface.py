import typing
import uuid

from fastup.domain import entities


class Authenticator(typing.Protocol):
    def authenticate(
        self,
        identifier: str,
        password: str,
    ) -> entities.Session: ...

    def verify_ticket(
        self, session_uuid: uuid.UUID, token: str
    ) -> entities.Session: ...


class PhoneAuthenticator:
    def __init__(self, sms_provider) -> None:
        self.sms_provider = sms_provider


class EmailAuthenticator:
    def __init__(self, hasher, email_provider) -> None:
        self.hasher = hasher
        self.email_provider = email_provider
