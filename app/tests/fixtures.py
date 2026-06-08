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
from logic.bus.base import ApplicationBus
from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
)


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

    def init_application_bus() -> ApplicationBus:
        application_bus = ApplicationBus()

        application_bus.register_command(
            CreateChatCommand,
            [
                CreateChatCommandHandler(
                    _command_bus=application_bus,
                    chats_repository=container.resolve(BaseChatsRepository),
                ),
            ],
        )

        application_bus.register_event(NewChatCreatedEvent, [])

        return application_bus

    container.register(ApplicationBus, factory=init_application_bus, scope=Scope.singleton)

    return container
