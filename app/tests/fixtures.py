from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.messages.base import BaseChatsRepository
from infrastructure.repositories.messages.memory import MemoryChatsRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(
        BaseChatsRepository,
        MemoryChatsRepository,
        scope=Scope.singleton,
    )
    return container
