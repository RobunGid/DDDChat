from dataclasses import dataclass
from typing import Any, Generic

from domain.entities.messages import Chat
from infrastructure.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.exceptions.messages import ChatNotFoundException
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetChatQuery(BaseQuery):
    chat_oid: str
    
@dataclass(frozen=True)
class GetChatQueryHandler(BaseQueryHandler, Generic[QT, QR]):
    chats_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository # TODO: Get messages independtly
    
    async def handle(self, query: GetChatQuery) -> Chat:
        chat = await self.chats_repository.get_chat_by_oid(oid=query.chat_oid)
  
        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        return chat