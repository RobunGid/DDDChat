from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Iterable,
)

from domain.events.base import BaseEvent
from logic.events.base import (
    EventHandler,
)


@dataclass(eq=False)
class EventBus[ET, ER](ABC):
    events_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        pass

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        pass
