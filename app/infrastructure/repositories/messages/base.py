from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import (
    Chat,
    Message,
)
from infrastructure.repositories.filters.messages import (
    GetChatsFilters,
    GetMessagesFilters,
)


@dataclass
class BaseChatsRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool:
        pass

    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        pass

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None:
        pass

    @abstractmethod
    async def get_chats(
        self,
        filters: GetChatsFilters,
    ) -> tuple[Iterable[Chat], int]:
        pass

    @abstractmethod
    async def delete_chat_by_oid(self, oid: str) -> None:
        pass

    @abstractmethod
    async def add_telegram_support_listener(self, chat_oid: str, telegram_chat_id: str) -> None:
        pass


@dataclass
class BaseMessagesRepository(ABC):
    @abstractmethod
    async def add_message(self, message: Message) -> None:
        pass

    @abstractmethod
    async def get_messages(
        self,
        chat_oid: str,
        filters: GetMessagesFilters,
    ) -> tuple[Iterable[Message], int]:
        pass
