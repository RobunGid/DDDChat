from dataclasses import dataclass

from dtos.chats import ChatMappingDataDTO
from exceptions.chats import ChatMappingDataAlreadyExistsException, ChatMappingDataNotFoundException
from repositories.chats.base import BaseChatsRepository


@dataclass(eq=False)
class ChatsStorageService:
    repository: BaseChatsRepository

    async def add_chat_mapping_data(self, telegram_chat_id: str, web_chat_id: str) -> ChatMappingDataDTO:
        if await self.repository.check_is_chat_mapping_data_exists(
            web_chat_id=web_chat_id,
            telegram_chat_id=telegram_chat_id,
        ):
            raise ChatMappingDataAlreadyExistsException(
                telegram_chat_id=telegram_chat_id,
                web_chat_id=web_chat_id,
            )

        return await self.repository.add_chat_mapping_data_exists(
            chat_mapping_data=ChatMappingDataDTO(
                web_chat_id=web_chat_id,
                telegram_chat_id=telegram_chat_id,
            ),
        )

    async def delete_chat_mapping_data_by_telegram_chat_id(self, telegram_chat_id: str):
        if not await self.repository.check_is_chat_mapping_data_exists(
            telegram_chat_id=telegram_chat_id,
        ):
            raise ChatMappingDataNotFoundException(
                telegram_chat_id=telegram_chat_id,
            )

        await self.repository.delete_chat_mapping_data_by_telegram_chat_id(
            telegram_chat_id=telegram_chat_id,
        )

    async def delete_chat_mapping_data_by_web_chat_id(self, web_chat_id: str):
        if not await self.repository.check_is_chat_mapping_data_exists(
            web_chat_id=web_chat_id,
        ):
            raise ChatMappingDataNotFoundException(
                web_chat_id=web_chat_id,
            )

        await self.repository.delete_chat_by_web_chat_id(
            web_chat_id=web_chat_id,
        )

    # TODO: Change all telegram_chat_id to telegram_thread_id
    async def get_chat_mapping_data_by_telegram_id(self, telegram_chat_id: str) -> ChatMappingDataDTO:
        if not await self.repository.check_is_chat_mapping_data_exists(
            telegram_chat_id=telegram_chat_id,
        ):
            raise ChatMappingDataNotFoundException(telegram_chat_id=telegram_chat_id)

        return await self.repository.get_by_telegram_id(telegram_chat_id=telegram_chat_id)

    async def get_chat_mapping_data_by_web_chat_id(self, web_chat_id: str) -> ChatMappingDataDTO:
        if not await self.repository.check_is_chat_mapping_data_exists(web_chat_id=web_chat_id):
            raise ChatMappingDataNotFoundException(web_chat_id=web_chat_id)

        return await self.repository.get_by_web_id(web_chat_id=web_chat_id)
