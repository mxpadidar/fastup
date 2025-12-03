import datetime
import typing
import uuid

import jwt


class InvalidTokenExc(Exception): ...


type TokenType = typing.Literal["access", "refresh", "signup"]


class Token(typing.NamedTuple):
    id: uuid.UUID
    raw: str
    sub: str
    typ: TokenType
    exp: datetime.datetime


class PyJWTService:
    """JWT-based token service for encoding and decoding tokens.

    This class handles the generation and validation of JSON Web Tokens (JWTs)
    for authentication and authorization. It uses PyJWT for encoding/decoding.
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        leeway: datetime.timedelta = datetime.timedelta(minutes=1),
    ):
        """Initialize the JwtTokenService with configuration parameters.

        :param secret_key: The secret key used to sign and verify tokens.
        :param algorithm: The algorithm used for token signing (default: HS256).
        :param leeway: The allowed clock skew for token validation (default: 1 minute).
        """
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._leeway = leeway

    def encode(self, sub: str, typ: TokenType, ttl: datetime.timedelta) -> Token:
        """Encode a new token for the given subject and type.

        :param sub: The subject identifier (e.g., user ID).
        :param typ: The type of token (e.g., access or refresh).
        :param ttl: The time-to-live duration for the token.
        :return: A Token object containing the encoded token details.
        """
        id = uuid.uuid4()
        exp = datetime.datetime.now(datetime.UTC) + ttl
        claims = {"sub": sub, "exp": exp.timestamp(), "typ": typ, "jti": id.hex}
        raw_token = jwt.encode(
            payload=claims, key=self._secret_key, algorithm=self._algorithm
        )
        return Token(id=id, raw=raw_token, sub=sub, typ=typ, exp=exp)

    def decode(self, raw_token: str) -> Token:
        """Decode and validate the given token.

        :param raw_token: The token string to decode and validate.
        :return: A Token object containing the decoded claims.
        :raises InvalidTokenExc: If the token is invalid or cannot be decoded.
        """
        try:
            claims = jwt.decode(
                jwt=raw_token,
                key=self._secret_key,
                algorithms=[self._algorithm],
                leeway=self._leeway,
            )
        except (jwt.PyJWTError, ValueError) as e:
            raise InvalidTokenExc from e

        try:
            return Token(
                id=uuid.UUID(claims["jti"]),
                raw=raw_token,
                sub=claims["sub"],
                typ=claims["typ"],
                exp=datetime.datetime.fromtimestamp(claims["exp"], datetime.UTC),
            )
        except (KeyError, ValueError) as e:
            raise InvalidTokenExc from e
