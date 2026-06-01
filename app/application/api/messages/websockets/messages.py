from uuid import UUID

from fastapi import Depends, WebSocket
from fastapi.routing import APIRouter
from punq import Container

from application.api.common.websockets.managers import BaseConnectionManager
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
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    config: Config = container.resolve(Config)
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    await connection_manager.accept_connection(websocket=websocket, key=chat_oid)
    
    try:
        async for message in message_broker.start_consuming(
            topic=config.new_message_received_event_topic
        ):
            await connection_manager.send_all(key=chat_oid, json_message=message)
    finally:
        await connection_manager.remove_connection(websocket=websocket, key=chat_oid)
        await message_broker.stop_consuming()