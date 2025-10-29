from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.errors import BaseErr


async def domain_errors_handler(request: Request, exc: BaseErr):
    """Handle domain-specific errors by returning a JSON response with error details."""
    return JSONResponse(
        status_code=exc.code,
        content=[{"detail": exc.message, **exc.extra}],
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors by formatting them into a list of error dicts."""
    errors_list = [
        {
            ".".join(str(part) for part in e["loc"]): e["type"],
            "detail": e["msg"],
            "ctx": e.get("ctx", {}),
        }
        for e in exc.errors()
    ]
    return JSONResponse(status_code=422, content=errors_list)
