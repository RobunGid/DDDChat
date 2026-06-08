from fastapi import Request, status
from fastapi.responses import JSONResponse

from domain.exceptions.base import (
    ApplicationConflictException,
    ApplicationNotFoundException,
    ApplicationValidationException,
)


async def conflict_exception_handler(
    request: Request,
    exception: ApplicationConflictException,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "status_code": status.HTTP_409_CONFLICT,
            "detail": {"error": exception.message},
        },
    )


async def not_found_exception_handler(
    request: Request,
    exception: ApplicationNotFoundException,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": {"error": exception.message},
        },
    )


async def validation_exception_handler(request: Request, exception: ApplicationValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "detail": {"error": exception.message},
        },
    )
