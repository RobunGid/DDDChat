from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from domain.entities.messages import Chat, Message
from infrastructure.repositories.filters.messages import GetChatsFilters, GetMessagesFilters
from infrastructure.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository


@dataclass
class MemoryChatsRepository(BaseChatsRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(chat for chat in self._saved_chats if chat.title.as_generic_type() == title),
            )
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        try:
            return next(chat for chat in self._saved_chats if chat.oid == oid)
        except StopIteration:
            return None

    async def get_chats(self, filters: GetChatsFilters) -> tuple[Iterable[Chat], int]:
        return self._saved_chats[filters.offset :][: filters.limit], len(self._saved_chats)

    async def delete_chat_by_oid(self, oid: str) -> None:
        self._saved_chats = [chat for chat in self._saved_chats if chat.oid != oid]


@dataclass
class MemoryMessagesRepository(BaseMessagesRepository):
    _saved_messages: list[Message] = field(default_factory=list, kw_only=True)

    async def get_messages(self, chat_oid: str, filters: GetMessagesFilters) -> tuple[Iterable[Message], int]:
        filtered_messages = [message for message in self._saved_messages if message.chat_oid == chat_oid]
        return filtered_messages[filters.offset :][: filters.limit], len(self._saved_messages)

    async def add_message(self, message: Message) -> None:
        return await super().add_message(message)
