from uuid import UUID

from fastapi import Depends, WebSocket
from fastapi.routing import APIRouter
from punq import Container

from infrastructure.message_brokers.base import BaseMessageBroker
from logic.init import init_container
from settings.config import Config


router = APIRouter(tags=["chats"])

@router.websocket("/{chat_oid}/")
async def message_handlers(
    websocket: WebSocket, 
    chat_oid: UUID,
    container: Container = Depends(init_container)
):
    await websocket.accept()
    
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    config: Config = container.resolve(Config)
    
    await message_broker.start_consuming(
        topic=config.new_message_received_event_topic.format(chat_oid=chat_oid)
    )
    
    while True:
        try:
            await websocket.send_json(await message_broker.consume())
        finally:
            break
    
    await message_broker.stop_consuming()
    await websocket.close()