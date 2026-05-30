from fastapi import FastAPI

from application.api.lifespan import lifespan
from application.api.messages.handlers import router as message_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="DDDChat with Kafka",
        docs_url="/api/docs",
        description="Kafka DDD chat",
        debug=True,
        lifespan=lifespan
    )
    app.include_router(message_router, prefix="/chat")

    return app