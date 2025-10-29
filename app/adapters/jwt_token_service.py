import datetime

import jwt

from app.domain import errors
from app.domain.dtos import TokenClaims
from app.domain.enums import TokenType


class JwtTokenService:
    """JWT-based implementation of the TokenService protocol.

    This class handles the generation and validation of JSON Web Tokens (JWTs)
    for authentication and authorization. It uses PyJWT for encoding/decoding
    and supports standard claims like issuer (iss), subject (sub), audience (aud),
    expiration (exp), issued at (iat), and token type (typ).
    """

    def __init__(
        self,
        secret_key: str,
        issuer: str,
        audience: str,
        access_exp_delta: datetime.timedelta = datetime.timedelta(minutes=15),
        refresh_exp_delta: datetime.timedelta = datetime.timedelta(days=7),
        algorithm: str = "HS256",
        leeway: datetime.timedelta = datetime.timedelta(minutes=1),
    ):
        """Initialize the JwtTokenService with configuration parameters.

        :param secret_key: The secret key used to sign and verify tokens.
        :param issuer: The issuer claim (iss) for tokens.
        :param audience: The audience claim (aud) for tokens.
        :param access_exp_delta: The expiration time for access tokens (default: 15 minutes).
        :param refresh_exp_delta: The expiration time for refresh tokens (default: 7 days).
        :param algorithm: The algorithm used for token signing (default: HS256).
        :param leeway: The allowed clock skew for token validation (default: 1 minute).
        """

        self.secret_key = secret_key
        self.issuer = issuer
        self.audience = audience
        self.access_exp_delta = access_exp_delta
        self.refresh_exp_delta = refresh_exp_delta
        self.algorithm = algorithm
        self.leeway = leeway

    def encode(self, sub: str, token_type: TokenType) -> tuple[str, datetime.datetime]:
        """Encode a JWT token for the given subject and type.

        :param sub: The subject identifier (e.g., user ID).
        :param token_type: The type of token (access or refresh).
        :return: The encoded JWT token as a string and the expiration datetime.
        """
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        payload = TokenClaims(
            iss=self.issuer,
            sub=sub,
            aud=self.audience,
            iat=now,
            exp=now + self._get_exp_delta(token_type),
            typ=token_type,
        )

        token = jwt.encode(
            payload=payload.to_dict(),
            key=self.secret_key,
            algorithm=self.algorithm,
        )

        return token, payload.exp

    def decode(self, token: str, token_type: TokenType) -> TokenClaims:
        """Decode and validate a JWT token.

        :param token: The JWT token string to decode and validate.
        :param token_type: The expected token type.
        :return: A TokenClaims object with the decoded claims.
        :raises InvalidTokenErr: If the token is invalid, expired, or does not match the expected type.
        """
        try:
            claims = jwt.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                audience=self.audience,
                leeway=self.leeway,
                options={"require": ["exp", "iss", "sub", "typ", "jti", "aud"]},
            )
            token_data = TokenClaims.from_dict(claims)
        except (jwt.PyJWTError, errors.ValidationErr) as e:
            raise errors.InvalidTokenErr("Invalid token") from e

        if token_data.typ != token_type:
            raise errors.InvalidTokenErr("Invalid token type")

        return token_data

    def _get_exp_delta(self, token_type: TokenType) -> datetime.timedelta:
        """Get the expiration delta for the given token type.

        :param token_type: The type of token (access or refresh).
        :return: The expiration delta as a timedelta.
        """
        return (
            self.access_exp_delta
            if token_type == TokenType.ACCESS
            else self.refresh_exp_delta
        )
