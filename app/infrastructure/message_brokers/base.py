
from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer
from aiokafka.producer import AIOKafkaProducer


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self):
        pass
    
    @abstractmethod
    async def close(self):
        pass
    
    @abstractmethod
    async def send_message(self, topic: str, value: bytes, key: bytes):
        pass
        
    @abstractmethod
    async def start_consuming(self, topic: str):
        pass
    
    @abstractmethod
    async def stop_consuming(self):
        pass
    
    @abstractmethod
    async def consume(self, topic: str) -> dict:
        pass