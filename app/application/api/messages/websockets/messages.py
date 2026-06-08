from uuid import UUID

from fastapi import (
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.routing import APIRouter

from punq import Container

from infrastructure.websockets.managers import BaseConnectionManager
from logic.exceptions.messages import ChatNotFoundException
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.messages import GetChatQuery

router = APIRouter(tags=["chats"])


@router.websocket("/{chat_oid}/")
async def message_handlers(
    websocket: WebSocket,
    chat_oid: UUID,
    container: Container = Depends(init_container),
):
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    mediator = container.resolve(Mediator)

    try:
        await mediator.handle_query(GetChatQuery(chat_oid=str(chat_oid)))
    except ChatNotFoundException as exception:
        await websocket.accept()
        await websocket.send_json(data={"error": exception.message})
        await websocket.close()
        return

    await connection_manager.accept_connection(websocket=websocket, key=str(chat_oid))

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await connection_manager.remove_connection(
            websocket=websocket,
            key=str(chat_oid),
        )
