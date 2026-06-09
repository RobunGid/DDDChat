from punq import Container, Scope

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
    CreateMessageCommand,
    CreateMessageCommandHandler,
    DeleteChatCommand,
    DeleteChatCommandHandler,
)
from logic.queries.messages import (
    GetChatQuery,
    GetChatQueryHandler,
    GetChatsQuery,
    GetChatsQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)
from settings.config import Config

config = Config()


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

    container.register(GetChatQueryHandler)
    container.register(GetMessagesQueryHandler)
    container.register(GetChatsQueryHandler)

    def init_application_bus() -> ApplicationBus:
        application_bus = ApplicationBus()

        # Commands
        application_bus.register_command(
            CreateChatCommand,
            [
                CreateChatCommandHandler(
                    _command_bus=application_bus,
                    chats_repository=container.resolve(BaseChatsRepository),
                ),
            ],
        )
        application_bus.register_command(
            DeleteChatCommand,
            [
                DeleteChatCommandHandler(
                    _command_bus=application_bus,
                    chats_repository=container.resolve(BaseChatsRepository),
                ),
            ],
        )
        application_bus.register_command(
            CreateMessageCommand,
            [
                CreateMessageCommandHandler(
                    _command_bus=application_bus,
                    messages_repository=container.resolve(BaseMessagesRepository),
                    chats_repository=container.resolve(BaseChatsRepository),
                ),
            ],
        )
        # Queries
        application_bus.register_query(
            GetChatQuery,
            container.resolve(GetChatQueryHandler),
        )
        application_bus.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )
        application_bus.register_query(
            GetChatsQuery,
            container.resolve(GetChatsQueryHandler),
        )
        return application_bus

    container.register(ApplicationBus, factory=init_application_bus, scope=Scope.singleton)

    return container
