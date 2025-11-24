import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastup.core import exceptions

logger = logging.getLogger(__name__)

exc_map = {
    exceptions.NotFoundExc: status.HTTP_404_NOT_FOUND,
    exceptions.ConflictExc: status.HTTP_409_CONFLICT,
}


async def core_exception_handler(
    request: Request, exc: exceptions.BaseExc
) -> JSONResponse:
    """Handles custom domain-layer exceptions using a scalable, mapper-driven approach.

    This function maps domain exception types to HTTP status codes, providing a
    central point of control for handling business logic errors.
    """
    exc_type = type(exc)
    status_code = exc_map.get(exc_type)
    if status_code is None:
        logger.critical(f"Unmapped domain exception caught: {exc_type.__name__}")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return JSONResponse(
        status_code=status_code,
        content={
            "errors": [exc.message],
            "extra": [exc.extra] if exc.extra else [],
        },
    )


def http_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handles Pydantic's RequestValidationError to provide a clean, standard error response.

    This handler intercepts the default FastAPI 422 error and transforms it into a
    400 Bad Request response with a structured JSON body, which is often preferred
    for client-side validation errors.
    """
    messages = [err["msg"] for err in exc.errors()]
    extra = [
        {
            "field": ".".join(str(loc) for loc in err["loc"]),
            "message": err["msg"],
            "type": err["type"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"errors": messages, "extra": extra},
    )
