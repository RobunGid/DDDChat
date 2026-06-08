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

from logic.bus.event import EventBus


@dataclass(frozen=True)
class BaseCommand(ABC):
    pass


CT = TypeVar("CT", bound=BaseCommand)  # Command Type
CR = TypeVar("CR", bound=Any)  # Command Result


@dataclass(frozen=True)
class CommandHandler(ABC, Generic[CT, CR]):
    _command_bus: EventBus

    @abstractmethod
    async def handle(self, command: CT) -> CR:
        pass
