from abc import ABC, abstractmethod
from dataclasses import dataclass

from dtos.chats import ChatDTO, ChatMappingDataDTO
from httpx import AsyncClient

from repositories.chats.base import BaseChatsRepository


@dataclass
class BaseChatWebService(ABC):
    http_client: AsyncClient
    base_url: str

    @abstractmethod
    async def get_all_chats(self) -> list[ChatDTO]:
        pass

    @abstractmethod
    async def get_chat(self, chat_oid: str) -> ChatDTO:
        pass

    @abstractmethod
    async def create_message_in_chat(self, chat_oid: str, message_text: str):
        pass


@dataclass
class BaseChatsStorageService(ABC):
    repository: BaseChatsRepository

    @abstractmethod
    async def add_chat_mapping_data(
        self,
        telegram_thread_id: str,
        web_chat_id: str,
    ) -> ChatMappingDataDTO:
        pass

    @abstractmethod
    async def delete_chat_mapping_data_by_telegram_thread_id(
        self,
        telegram_thread_id: str,
    ) -> None:
        pass

    @abstractmethod
    async def delete_chat_mapping_data_by_web_chat_id(
        self,
        web_chat_id: str,
    ) -> None:
        pass

    @abstractmethod
    async def get_chat_mapping_data_by_telegram_thread_id(
        self,
        telegram_thread_id: str,
    ) -> ChatMappingDataDTO:
        pass

    @abstractmethod
    async def get_chat_mapping_data_by_web_chat_id(
        self,
        web_chat_id: str,
    ) -> ChatMappingDataDTO:
        pass
