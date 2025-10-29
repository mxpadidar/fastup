import dataclasses
import datetime
import uuid

from app.domain import enums, errors


@dataclasses.dataclass
class TokenClaims:
    """Represents the payload of a JWT token with standard claims.

    iss: The issuer of the token (string identifier).
    sub: The subject of the token (e.g., user ID).
    aud: The audience for which the token is intended.
    iat: The time at which the token was issued (datetime).
    exp: The expiration time of the token (datetime).
    typ: The type of token (access or refresh).
    jti: Unique identifier for the token (UUID).
    """

    iss: str
    sub: str
    aud: str
    iat: datetime.datetime
    exp: datetime.datetime
    typ: enums.TokenType
    jti: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, data: dict) -> "TokenClaims":
        """Create a TokenPayload instance from a dictionary.

        :param data: Dictionary containing the JWT claims with integer timestamps.
        :return: A new TokenPayload instance.
        :raises ValidationErr: If required keys are missing or claim values are invalid.
        """
        try:
            sub = data["sub"]
            if not sub.strip():
                raise ValueError("sub cannot be empty")

            return cls(
                iss=data["iss"],
                sub=sub,
                aud=data["aud"],
                iat=datetime.datetime.fromtimestamp(
                    data["iat"], tz=datetime.timezone.utc
                ),
                exp=datetime.datetime.fromtimestamp(
                    data["exp"], tz=datetime.timezone.utc
                ),
                typ=enums.TokenType(data["typ"]),
                jti=uuid.UUID(data["jti"]),
            )
        except (KeyError, ValueError, TypeError) as e:
            raise errors.ValidationErr from e

    def to_dict(self) -> dict:
        """Convert the TokenPayload to a dictionary for JWT encoding.

        :return: A dictionary with integer timestamps for time claims.
        """
        return {
            "iss": self.iss,
            "sub": self.sub,
            "aud": self.aud,
            "iat": int(self.iat.timestamp()),
            "exp": int(self.exp.timestamp()),
            "typ": self.typ.value,
            "jti": self.jti.hex,
        }
