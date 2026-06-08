from contextlib import asynccontextmanager

from fastapi import FastAPI

from aiojobs import Scheduler
from punq import Container

from application.api.exception_handlers import (
    conflict_exception_handler,
    not_found_exception_handler,
    validation_exception_handler,
)
from application.api.lifespan import (
    close_message_broker,
    consumer_in_background,
    init_message_broker,
)
from application.api.messages.handlers import router as message_router
from application.api.messages.websockets.messages import router as message_ws_router
from domain.exceptions.base import (
    ApplicationConflictException,
    ApplicationNotFoundException,
    ApplicationValidationException,
)
from logic.init import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()
    container: Container = init_container()
    scheduler: Scheduler = container.resolve(Scheduler)
    job = await scheduler.spawn(consumer_in_background())

    yield

    await close_message_broker()
    await job.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDDChat with Kafka",
        docs_url="/api/docs",
        description="Kafka DDD chat",
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(message_router, prefix="/chats")
    app.include_router(message_ws_router, prefix="/chats")

    app.add_exception_handler(ApplicationValidationException, validation_exception_handler)
    app.add_exception_handler(ApplicationConflictException, conflict_exception_handler)
    app.add_exception_handler(ApplicationNotFoundException, not_found_exception_handler)

    return app
