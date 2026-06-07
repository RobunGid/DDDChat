from dataclasses import dataclass

from dtos.messages import ChatDataDTO
from exceptions.chats import ChatAlreadyExistsException
from repositories.chats.base import BaseChatsRepository


@dataclass(eq=False)
class ChatsService:
    repository: BaseChatsRepository

    async def add_chat(self, telegram_chat_id: str, web_chat_id: str) -> ChatDataDTO:
        if await self.repository.check_is_chat_exists(
            web_chat_id=web_chat_id,
            telegram_chat_id=telegram_chat_id,
        ):
            raise ChatAlreadyExistsException(
                telegram_chat_id=telegram_chat_id,
                web_chat_id=web_chat_id,
            )

        return await self.repository.add_chat(
            chat_info=ChatDataDTO(
                web_chat_id=web_chat_id,
                telegram_chat_id=telegram_chat_id,
            ),
        )
