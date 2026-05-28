from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.events.base import BaseEvent

ET = TypeVar("ET", bound=BaseEvent) # Event Type
ER = TypeVar("ER", bound=Any) # Event Result

@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    def handle(self, event: ET) -> ER:
        ...