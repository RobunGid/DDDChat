from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import (
    Chat,
    ChatListener,
    Message,
)
from infrastructure.repositories.filters.messages import (
    GetChatsFilters,
    GetMessagesFilters,
)
from infrastructure.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from logic.exceptions.messages import ChatNotFoundException
from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
)


@dataclass(frozen=True)
class GetChatQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessagesFilters


@dataclass(frozen=True)
class GetChatsQuery(BaseQuery):
    filters: GetChatsFilters


@dataclass(frozen=True)
class GetChatListenersQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetChatQueryHandler(BaseQueryHandler[GetChatQuery, Chat]):
    chats_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository  # TODO: Get messages independtly

    async def handle(self, query: GetChatQuery) -> Chat:
        chat = await self.chats_repository.get_chat_by_oid(oid=query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        return chat


@dataclass(frozen=True)
class GetMessagesQueryHandler(
    BaseQueryHandler[GetMessagesQuery, tuple[Iterable[Message], int]],
):
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetMessagesQuery) -> tuple[Iterable[Message], int]:
        # TODO: Reading messages events
        messages, count = await self.messages_repository.get_messages(
            chat_oid=query.chat_oid,
            filters=query.filters,
        )
        return messages, count


@dataclass(frozen=True)
class GetChatsQueryHandler(
    BaseQueryHandler[
        GetChatsQuery,
        tuple[Iterable[Chat], int],
    ],
):
    chats_repository: BaseChatsRepository

    async def handle(self, query: GetChatsQuery) -> tuple[Iterable[Chat], int]:
        chat, count = await self.chats_repository.get_chats(
            filters=query.filters,
        )
        return chat, count


@dataclass(frozen=True)
class GetChatListenersQueryHandler(
    BaseQueryHandler[
        GetChatListenersQuery,
        Iterable[ChatListener],
    ],
):
    chats_repository: BaseChatsRepository

    async def handle(self, query: GetChatListenersQuery) -> Iterable[ChatListener]:
        # TODO: remove 2 request to db
        chat = await self.chats_repository.get_chat_by_oid(oid=query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        listeners = await self.chats_repository.get_chat_listeners(chat_oid=query.chat_oid)
        return listeners
