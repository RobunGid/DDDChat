from fastapi import Request, status
from fastapi.responses import JSONResponse

from logic.exceptions.messages import ChatNotFoundException, ChatWithThatTitleAlreadyExistsException


async def chat_not_found_exception_handler(request: Request, exception: ChatNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": {"error": exception.message},
        },
    )


async def chat_with_that_title_already_exists_exception_handler(
    request: Request,
    exception: ChatWithThatTitleAlreadyExistsException,
):
    return JSONResponse(
        status_code=404,
        content={
            "status_code": status.HTTP_409_CONFLICT,
            "detail": {"error": exception.message},
        },
    )
