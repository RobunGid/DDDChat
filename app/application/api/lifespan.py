from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.message_brokers.base import BaseMessageBroker
from logic.init import init_container

async def start_kafka():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.producer.start()
    
    
async def stop_kafka():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.producer.stop()
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_kafka()
    yield
    await stop_kafka()