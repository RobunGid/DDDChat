from uuid import UUID

from fastapi import (
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.routing import APIRouter

from infrastructure.websockets.managers import BaseConnectionManager
from logic.init import init_container
from punq import Container

router = APIRouter(tags=["chats"])


@router.websocket("/{chat_oid}/")
async def message_handlers(
    websocket: WebSocket,
    chat_oid: UUID,
    container: Container = Depends(init_container),
):
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    await connection_manager.accept_connection(websocket=websocket, key=str(chat_oid))

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await connection_manager.remove_connection(
            websocket=websocket,
            key=str(chat_oid),
        )
