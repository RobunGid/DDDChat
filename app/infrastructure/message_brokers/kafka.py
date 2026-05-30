
from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    
    async def send_message(self, topic: str, value: bytes, key: bytes):
        await self.producer.send(topic=topic, value=value, key=key)
        
    async def consume(self, topic: str):
        ...