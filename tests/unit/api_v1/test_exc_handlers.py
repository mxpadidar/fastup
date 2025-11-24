import json
from types import SimpleNamespace

import pytest
from fastapi import status
from fastapi.exceptions import RequestValidationError

from fastup.api.v1 import exc_handlers
from fastup.core import exceptions


@pytest.fixture
def fake_request():
    """Provides a minimal fake request object to satisfy exc handler signatures."""
    return SimpleNamespace(method="POST", url="http://testserver/test")


def test_validation_handler_returns_structured_400(fake_request):
    """Should return a 400 response with a correctly structured error payload"""
    # Arrange
    validation_exc = RequestValidationError(
        errors=[
            {
                "loc": ("body", "phone"),
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    )
    # Act
    response = exc_handlers.http_validation_exception_handler(
        fake_request, validation_exc
    )
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    payload = json.loads(response.body)  # type: ignore
    assert "errors" in payload and "extra" in payload
    assert isinstance(payload["errors"], list)
    assert isinstance(payload["extra"], list)
    assert payload["extra"][0]["field"] == "body.phone"
    assert payload["extra"][0]["message"] == "field required"
    assert payload["extra"][0]["type"] == "value_error.missing"


@pytest.mark.parametrize(
    "exc, expected_status",
    [
        (exc_class(), status_code)
        for exc_class, status_code in exc_handlers.exc_map.items()
    ],
)
async def test_domain_exception_handler_returns_expected_status_and_message(
    fake_request, exc: exceptions.BaseExc, expected_status: int
):
    """Should return the correct HTTP status and payload for mapped domain exceptions."""
    response = await exc_handlers.core_exception_handler(fake_request, exc)
    assert response.status_code == expected_status

    payload = json.loads(response.body)  # type: ignore
    assert "errors" in payload and "extra" in payload
    assert isinstance(payload["errors"], list)
    assert isinstance(payload["extra"], list)


async def test_domain_exception_handler_unmapped_error_returns_500(fake_request):
    """Should return 500 Internal Server Error if the exception type is unmapped."""

    class UnmappedExc(exceptions.BaseExc): ...

    exc = UnmappedExc(message="Unexpected error!")
    response = await exc_handlers.core_exception_handler(fake_request, exc)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    payload = json.loads(response.body)  # type: ignore
    assert payload["errors"][0] == "Unexpected error!"
