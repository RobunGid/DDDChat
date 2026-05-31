from fastapi import WebSocket
from fastapi.routing import APIRouter

router = APIRouter(tags=["chats"])

@router.websocket("{chat_oid}")
async def message_handlers(websocket: WebSocket, chat_oid: str):
    await websocket.accept()
    