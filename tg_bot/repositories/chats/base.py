from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import overload

from aiosqlite import connect
from dtos.chats import ChatDataDTO
from exceptions.chats import ChatDataNotFoundException
from repositories.queries import (
    ADD_NEW_CHAT_DATA_SQL_QUERY,
    GET_CHAT_DATA_BY_TELEGRAM_ID_SQL_QUERY,
    GET_CHAT_DATA_BY_WEB_ID_SQL_QUERY,
    GET_CHATS_COUNT_SQL_QUERY,
)


class BaseChatsRepository(ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_chat_id: str) -> ChatDataDTO:
        pass

    @abstractmethod
    async def get_by_web_id(self, web_chat_id: str) -> ChatDataDTO:
        pass

    @overload
    @abstractmethod
    async def check_is_chat_exists(
        self,
        *,
        telegram_chat_id: str,
    ) -> bool:
        pass

    @overload
    @abstractmethod
    async def check_is_chat_exists(
        self,
        *,
        web_chat_id: str,
    ) -> bool:
        pass

    @overload
    @abstractmethod
    async def check_is_chat_exists(
        self,
        *,
        web_chat_id: str,
        telegram_chat_id: str,
    ) -> bool:
        pass

    @abstractmethod
    async def add_chat(self, chat_data: ChatDataDTO) -> ChatDataDTO:
        pass


@dataclass(eq=False)
class SQLChatsRepository(BaseChatsRepository):
    database_url: str

    async def add_chat(self, chat_data: ChatDataDTO) -> ChatDataDTO:
        async with connect(self.database_url) as connection:
            await connection.execute_insert(
                ADD_NEW_CHAT_DATA_SQL_QUERY,
                (chat_data.web_chat_id, chat_data.telegram_chat_id),
            )
            await connection.commit()

        return ChatDataDTO(
            web_chat_id=chat_data.web_chat_id,
            telegram_chat_id=chat_data.telegram_chat_id,
        )

    async def get_by_telegram_id(self, telegram_chat_id: str) -> ChatDataDTO:
        async with connect(self.database_url) as connection:
            cursor = await connection.execute(GET_CHAT_DATA_BY_TELEGRAM_ID_SQL_QUERY, (telegram_chat_id,))
            result = await cursor.fetchone()

        if result is None:
            raise ChatDataNotFoundException(telegram_chat_id=telegram_chat_id)

        return ChatDataDTO(
            web_chat_id=result[0],
            telegram_chat_id=str(result[1]),
        )

    async def get_by_web_id(self, web_chat_id: str) -> ChatDataDTO:
        async with connect(self.database_url) as connection:
            cursor = await connection.execute(GET_CHAT_DATA_BY_WEB_ID_SQL_QUERY, (web_chat_id,))
            result = await cursor.fetchone()

        if result is None:
            raise ChatDataNotFoundException(web_chat_id=web_chat_id)

        return ChatDataDTO(
            telegram_chat_id=result[0],
            web_chat_id=result[1],
        )

    async def check_is_chat_exists(
        self,
        web_chat_id: str | None = None,
        telegram_chat_id: str | None = None,
    ) -> bool:
        async with connect(self.database_url) as connection:
            cursor = await connection.execute(GET_CHATS_COUNT_SQL_QUERY, (web_chat_id, telegram_chat_id))
            result = await cursor.fetchone()

        if result is None:
            return False

        return result[0] > 0
