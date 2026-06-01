from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from domain.events.base import BaseEvent
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.websockets.managers import BaseConnectionManager

ET = TypeVar("ET", bound=BaseEvent)  # Event Type
ER = TypeVar("ER", bound=Any)  # Event Result


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    connection_manager: BaseConnectionManager
    broker_topic: str

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        pass
