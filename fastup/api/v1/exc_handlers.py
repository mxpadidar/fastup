import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastup.core import exceptions

logger = logging.getLogger(__name__)


def http_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handles Pydantic's RequestValidationError to provide a clean, standard error response.

    This handler intercepts the default FastAPI 422 error and transforms it into a
    400 Bad Request response with a structured JSON body, which is often preferred
    for client-side validation errors.
    """
    error_details = [
        {
            "field": ".".join(str(loc) for loc in err["loc"]),
            "message": err["msg"],
            "type": err["type"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"errors": error_details},
    )


async def core_exception_handler(
    request: Request, exc: exceptions.BaseExc
) -> JSONResponse:
    """
    Handles custom domain-layer exceptions using a scalable, mapper-driven approach.

    This function maps domain exception types to HTTP status codes, providing a
    central point of control for handling business logic errors.

    If an exception is not found in the map, it defaults to a 500 Internal
    Server Error and logs a critical error for immediate attention.

    The response format is a single JSON object with an 'error' key, providing a
    consistent structure for all domain-related errors.
    """
    match type(exc):
        case exceptions.NotFoundExc:
            status_code = status.HTTP_404_NOT_FOUND
        case exceptions.ConflictExc:
            status_code = status.HTTP_409_CONFLICT
        case _:
            logger.critical(f"Unmapped domain exception caught: {type(exc).__name__}")
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return JSONResponse(
        status_code=status_code,
        content={"error": {"message": exc.message, **exc.extra}},
    )
