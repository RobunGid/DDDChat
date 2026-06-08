from dataclasses import dataclass

from dtos.chats import ChatMappingDataDTO
from exceptions.chats import ChatMappingDataAlreadyExistsException, ChatMappingDataNotFoundException

from services.base import BaseChatsStorageService


@dataclass(eq=False)
class ChatsStorageService(BaseChatsStorageService):
    async def add_chat_mapping_data(self, telegram_thread_id: str, web_chat_id: str) -> ChatMappingDataDTO:
        if await self.repository.check_is_chat_mapping_data_exists(
            web_chat_id=web_chat_id,
            telegram_thread_id=telegram_thread_id,
        ):
            raise ChatMappingDataAlreadyExistsException(
                telegram_thread_id=telegram_thread_id,
                web_chat_id=web_chat_id,
            )

        return await self.repository.add_chat_mapping_data_exists(
            chat_mapping_data=ChatMappingDataDTO(
                web_chat_id=web_chat_id,
                telegram_thread_id=telegram_thread_id,
            ),
        )

    async def delete_chat_mapping_data_by_telegram_thread_id(self, telegram_thread_id: str):
        if not await self.repository.check_is_chat_mapping_data_exists(
            telegram_thread_id=telegram_thread_id,
        ):
            raise ChatMappingDataNotFoundException(
                telegram_thread_id=telegram_thread_id,
            )

        await self.repository.delete_chat_mapping_data_by_telegram_thread_id(
            telegram_thread_id=telegram_thread_id,
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

    async def get_chat_mapping_data_by_telegram_thread_id(self, telegram_thread_id: str) -> ChatMappingDataDTO:
        if not await self.repository.check_is_chat_mapping_data_exists(
            telegram_thread_id=telegram_thread_id,
        ):
            raise ChatMappingDataNotFoundException(telegram_thread_id=telegram_thread_id)

        return await self.repository.get_by_telegram_thread_id(telegram_thread_id=telegram_thread_id)

    async def get_chat_mapping_data_by_web_chat_id(self, web_chat_id: str) -> ChatMappingDataDTO:
        if not await self.repository.check_is_chat_mapping_data_exists(web_chat_id=web_chat_id):
            raise ChatMappingDataNotFoundException(web_chat_id=web_chat_id)

        return await self.repository.get_by_web_id(web_chat_id=web_chat_id)
