from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.events.base import BaseEvent
from infrastructure.message_brokers.base import BaseMessageBroker

ET = TypeVar("ET", bound=BaseEvent) # Event Type
ER = TypeVar("ER", bound=Any) # Event Result

@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    broker_topic: str | None = None
    
    def handle(self, event: ET) -> ER:
        ...