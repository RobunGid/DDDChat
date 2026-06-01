from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    cast,
    Generic,
    Iterable,
    Type,
)

from domain.events.base import BaseEvent
from logic.commands.base import (
    BaseCommand,
    CommandHandler,
    CR,
    CT,
)
from logic.events.base import (
    ER,
    ET,
    EventHandler,
)
from logic.exceptions.mediator import CommandHandlersNotRegisteredException
from logic.mediator.command import CommandMediator
from logic.mediator.event import EventMediator
from logic.mediator.query import QueryMediator
from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
    QR,
    QT,
)


@dataclass(eq=False)
class Mediator(
    EventMediator,
    QueryMediator,
    CommandMediator,
    Generic[ET, ER, QT, QR, CT, CR],
):
    events_map: dict[Type[ET], list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    commands_map: dict[Type[CT], list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    queries_map: dict[Type[QT], BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event.__class__].extend(event_handlers)

    def register_command(
        self,
        command: CT,
        command_handlers: Iterable[CommandHandler[CT, CR]],
    ):
        self.commands_map[command.__class__].extend(command_handlers)

    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]):
        self.queries_map[query.__class__] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers: Iterable[EventHandler] = self.events_map[
                cast(Type[ET], event.__class__)
            ]
            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        handlers = self.commands_map.get(cast(Type[CT], command.__class__))
        if not handlers:
            raise CommandHandlersNotRegisteredException(command.__class__)
        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QR:
        return await self.queries_map[cast(Type[QT], query.__class__)].handle(
            query=query,
        )
