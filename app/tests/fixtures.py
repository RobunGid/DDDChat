from punq import Container, Scope

from domain.events.messages import NewChatCreatedEvent
from infrastructure.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from infrastructure.repositories.messages.memory import (
    MemoryChatsRepository,
    MemoryMessagesRepository,
)
from infrastructure.websockets.managers import BaseConnectionManager, ConnectionManager
from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
)
from logic.mediator.base import Mediator


def init_dummy_container() -> Container:
    container = Container()

    container.register(
        BaseChatsRepository,
        instance=MemoryChatsRepository(),
        scope=Scope.singleton,
    )
    container.register(
        BaseMessagesRepository,
        instance=MemoryMessagesRepository(),
        scope=Scope.singleton,
    )

    container.register(
        BaseConnectionManager,
        instance=ConnectionManager(),
        scope=Scope.singleton,
    )

    def init_mediator() -> Mediator:
        mediator = Mediator()

        mediator.register_command(
            CreateChatCommand,
            [
                CreateChatCommandHandler(
                    _mediator=mediator,
                    chats_repository=container.resolve(BaseChatsRepository),
                ),
            ],
        )

        mediator.register_event(NewChatCreatedEvent, [])

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
