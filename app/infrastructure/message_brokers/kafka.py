
from dataclasses import dataclass, field
from typing import AsyncIterator

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import orjson

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer
    
    async def send_message(self, topic: str, value: bytes, key: bytes):
        await self.producer.send(topic=topic, value=value, key=key)
        
    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])
        
        async for message in self.consumer:
            yield orjson.loads(message.value)
        
    async def stop_consuming(self):
        self.consumer.unsubscribe()
        
    async def close(self):
        await self.producer.stop()
        await self.consumer.stop()
        
    async def start(self):
        await self.producer.start()
        await self.consumer.start()