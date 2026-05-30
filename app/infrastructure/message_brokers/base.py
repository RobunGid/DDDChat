
from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer
from aiokafka.producer import AIOKafkaProducer


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def send_message(self, topic: str, value: bytes, key: bytes):
        ...
        
    @abstractmethod
    async def consume(self, topic: str):
        ...