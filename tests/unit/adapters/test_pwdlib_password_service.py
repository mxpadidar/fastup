import pytest

from app.domain.protocols import PasswordService


def test_password_srvc_hash_password(password_service: PasswordService):
    password = "secure_password"
    password_hash = password_service.hash_password(password)
    assert isinstance(password_hash, str)
    assert password_hash != password


def test_password_srvc_verify_password_correct_password(
    password_service: PasswordService,
):
    password = "secure_password"
    password_hash = password_service.hash_password(password)
    assert password_service.verify_password(password, password_hash) is True


def test_password_srvc_verify_password_incorrect_password(
    password_service: PasswordService,
):
    password = "secure_password"
    password_hash = password_service.hash_password(password)
    assert password_service.verify_password("wrong_password", password_hash) is False


def test_password_srvc_verify_password__invalid_inputs(
    password_service: PasswordService,
):
    password = "secure_password"
    password_hash = password_service.hash_password(password)
    with pytest.raises(TypeError):
        password_service.verify_password(None, password_hash)  # type: ignore

    with pytest.raises(TypeError):
        password_service.verify_password(password, None)  # type: ignore


def test_password_srvc_hash_password_non_string_input(
    password_service: PasswordService,
):
    with pytest.raises(TypeError):
        password_service.hash_password(None)  # type: ignore
