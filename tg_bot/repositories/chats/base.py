from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import overload

from aiosqlite import connect
from dtos.chats import ChatMappingDataDTO
from exceptions.chats import ChatMappingDataNotFoundException

from repositories.queries import (
    ADD_NEW_CHAT_MAPPING_DATA_SQL_QUERY,
    DELETE_CHAT_MAPPING_DATA_BY_TELEGRAM_THREAD_ID_SQL_QUERY,
    DELETE_CHAT_MAPPING_DATA_BY_WEB_CHAT_ID_SQL_QUERY,
    GET_CHAT_MAPPING_DATA_BY_TELEGRAM_THREAD_ID_SQL_QUERY,
    GET_CHAT_MAPPING_DATA_BY_WEB_ID_SQL_QUERY,
    GET_CHAT_MAPPING_DATA_COUNT_SQL_QUERY,
)


class BaseChatsRepository(ABC):
    @abstractmethod
    async def get_by_telegram_thread_id(self, telegram_thread_id: str) -> ChatMappingDataDTO:
        pass

    @abstractmethod
    async def get_by_web_id(self, web_chat_id: str) -> ChatMappingDataDTO:
        pass

    @overload
    @abstractmethod
    async def check_is_chat_mapping_data_exists(
        self,
        *,
        telegram_thread_id: str,
    ) -> bool:
        pass

    @overload
    @abstractmethod
    async def check_is_chat_mapping_data_exists(
        self,
        *,
        web_chat_id: str,
    ) -> bool:
        pass

    @overload
    @abstractmethod
    async def check_is_chat_mapping_data_exists(
        self,
        *,
        web_chat_id: str,
        telegram_thread_id: str,
    ) -> bool:
        pass

    @abstractmethod
    async def add_chat_mapping_data_exists(self, chat_mapping_data: ChatMappingDataDTO) -> ChatMappingDataDTO:
        pass

    @abstractmethod
    async def delete_chat_mapping_data_by_telegram_thread_id(
        self,
        *,
        telegram_thread_id: str,
    ) -> None:
        pass

    @abstractmethod
    async def delete_chat_by_web_chat_id(
        self,
        *,
        web_chat_id: str,
    ) -> None:
        pass


@dataclass(eq=False)
class SQLChatsRepository(BaseChatsRepository):
    database_url: str

    async def add_chat_mapping_data_exists(self, chat_mapping_data: ChatMappingDataDTO) -> ChatMappingDataDTO:
        async with connect(self.database_url) as connection:
            await connection.execute_insert(
                ADD_NEW_CHAT_MAPPING_DATA_SQL_QUERY,
                (chat_mapping_data.web_chat_id, chat_mapping_data.telegram_thread_id),
            )
            await connection.commit()

        return ChatMappingDataDTO(
            web_chat_id=chat_mapping_data.web_chat_id,
            telegram_thread_id=chat_mapping_data.telegram_thread_id,
        )

    async def get_by_telegram_thread_id(self, telegram_thread_id: str) -> ChatMappingDataDTO:
        async with connect(self.database_url) as connection:
            cursor = await connection.execute(
                GET_CHAT_MAPPING_DATA_BY_TELEGRAM_THREAD_ID_SQL_QUERY,
                (telegram_thread_id,),
            )
            result = await cursor.fetchone()

        if result is None:
            raise ChatMappingDataNotFoundException(telegram_thread_id=telegram_thread_id)

        return ChatMappingDataDTO(
            web_chat_id=result[0],
            telegram_thread_id=str(result[1]),
        )

    async def get_by_web_id(self, web_chat_id: str) -> ChatMappingDataDTO:
        async with connect(self.database_url) as connection:
            cursor = await connection.execute(GET_CHAT_MAPPING_DATA_BY_WEB_ID_SQL_QUERY, (web_chat_id,))
            result = await cursor.fetchone()

        if result is None:
            raise ChatMappingDataNotFoundException(web_chat_id=web_chat_id)

        return ChatMappingDataDTO(
            web_chat_id=result[0],
            telegram_thread_id=str(result[1]),
        )

    async def check_is_chat_mapping_data_exists(
        self,
        web_chat_id: str | None = None,
        telegram_thread_id: str | None = None,
    ) -> bool:
        async with connect(self.database_url) as connection:
            cursor = await connection.execute(GET_CHAT_MAPPING_DATA_COUNT_SQL_QUERY, (web_chat_id, telegram_thread_id))
            result = await cursor.fetchone()

        if result is None:
            return False

        return result[0] > 0

    async def delete_chat_mapping_data_by_telegram_thread_id(self, *, telegram_thread_id: str) -> None:
        async with connect(self.database_url) as connection:
            await connection.execute(DELETE_CHAT_MAPPING_DATA_BY_TELEGRAM_THREAD_ID_SQL_QUERY, (telegram_thread_id,))
            await connection.commit()

    async def delete_chat_by_web_chat_id(self, *, web_chat_id: str) -> None:
        async with connect(self.database_url) as connection:
            await connection.execute(DELETE_CHAT_MAPPING_DATA_BY_WEB_CHAT_ID_SQL_QUERY, (web_chat_id,))
            await connection.commit()
