from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    AsyncIterator,
)


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
    def start_consuming(self, topic: str) -> AsyncIterator[dict[str, Any]]:
        pass

    @abstractmethod
    async def stop_consuming(self):
        pass
