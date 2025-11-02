import dataclasses
import datetime
import typing

from fastup.domain import enums


@dataclasses.dataclass
class AuthTicket:
    """Represents a single-use verifier used to prove control of an identity or to
    authorize a short-lived operation (register, change password, reset password).

    Invariants:
    - token_hash: hashed secret only; raw token is ephemeral and not persisted.
    - If intent == REGISTER then user_id should typically be None.
    - If intent targets an existing account (RESET_PW, CHANGE_PWD) user_id must be present.
    - created_at set by factory/repository; domain should check expiry/attempts before consume.
    """

    id: int = dataclasses.field(init=False)
    user_id: int | None = None
    method: enums.AuthMethod
    intent: enums.AuthIntent
    token_hash: str
    attempts: int = 0
    ipaddr: str
    metadata: dict[str, typing.Any] = dataclasses.field(default_factory=dict)
    created_at: datetime.datetime = dataclasses.field(init=False)
    expires_at: datetime.datetime
    consumed_at: datetime.datetime | None = None
