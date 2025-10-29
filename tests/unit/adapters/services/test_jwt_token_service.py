import datetime
import time
import uuid

import jwt
import pytest

from app.adapters import JwtTokenService
from app.domain import errors
from app.domain.dtos import TokenClaims
from app.domain.enums import TokenType
from app.domain.protocols import TokenService


def test_token_srvc_encode(token_service: TokenService):
    token, _ = token_service.encode(sub="user123", token_type=TokenType.ACCESS)
    assert isinstance(token, str)
    assert len(token) > 0


def test_token_srvc_decode_valid_access_token(token_service: TokenService):
    token, _ = token_service.encode(sub="user123", token_type=TokenType.ACCESS)

    payload = token_service.decode(token, TokenType.ACCESS)
    assert isinstance(payload, TokenClaims)
    assert payload.sub == "user123"
    assert payload.typ == TokenType.ACCESS


def test_token_srvc_decode_expired_token():
    expired_service = JwtTokenService(
        secret_key="test_secret_key",
        issuer="test_issuer",
        audience="test_audience",
        access_exp_delta=datetime.timedelta(seconds=-1),  # Expired 1 second ago
        algorithm="HS256",
        leeway=datetime.timedelta(seconds=0),
    )
    token, _ = expired_service.encode(sub="user123", token_type=TokenType.ACCESS)

    time.sleep(1)
    with pytest.raises(errors.InvalidTokenErr):
        expired_service.decode(token, TokenType.ACCESS)


def test_token_srvc_decode_wrong_type(token_service: TokenService):
    token, _ = token_service.encode(sub="user123", token_type=TokenType.ACCESS)
    with pytest.raises(errors.InvalidTokenErr):
        token_service.decode(token, TokenType.REFRESH)


def test_token_srvc_decode_token_wrong_issuer(
    token_service: TokenService, monkeypatch: pytest.MonkeyPatch
):
    token, _ = token_service.encode(sub="user123", token_type=TokenType.ACCESS)
    monkeypatch.setattr(token_service, "issuer", "wrong_issuer")
    with pytest.raises(errors.InvalidTokenErr):
        token_service.decode(token, TokenType.ACCESS)


def test_token_srvc_decode_wrong_audience(
    token_service: TokenService, monkeypatch: pytest.MonkeyPatch
):
    token, _ = token_service.encode(sub="user123", token_type=TokenType.ACCESS)
    monkeypatch.setattr(token_service, "audience", "wrong_audience")
    with pytest.raises(errors.InvalidTokenErr):
        token_service.decode(token, TokenType.ACCESS)


def test_token_srvc_decode_tampered_token(token_service: TokenService):
    token, _ = token_service.encode(sub="user123", token_type=TokenType.ACCESS)

    # Tamper by changing a character in the payload part
    header, payload, signature = token.split(".")
    tampered_payload = payload[:-1] + ("x" if payload[-1] != "x" else "y")
    tampered_token = f"{header}.{tampered_payload}.{signature}"

    with pytest.raises(errors.InvalidTokenErr):
        token_service.decode(tampered_token, TokenType.ACCESS)


def test_token_srvc_decode_token_with_missing_required_claims(
    token_service: TokenService,
):
    # manually create a token missing 'aud'
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    payload = {
        "iss": "test_issuer",
        "sub": "user123",
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(minutes=15)).timestamp()),
        "typ": "access",
        "jti": str(uuid.uuid4()),
    }
    token = jwt.encode(payload, "test_secret_key", algorithm="HS256")

    with pytest.raises(errors.InvalidTokenErr):
        token_service.decode(token, TokenType.ACCESS)


def test_token_srvc_decode_token_with_invalid_signature(
    token_service: TokenService, monkeypatch: pytest.MonkeyPatch
):
    token, _ = token_service.encode(sub="user123", token_type=TokenType.ACCESS)
    monkeypatch.setattr(token_service, "secret_key", "invalid_secret_key")
    with pytest.raises(errors.InvalidTokenErr):
        token_service.decode(token, TokenType.ACCESS)
