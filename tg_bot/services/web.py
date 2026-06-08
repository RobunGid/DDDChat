from abc import ABC, abstractmethod
from dataclasses import dataclass
from urllib.parse import urljoin

from dtos.chats import ChatDTO, ChatListenerDTO
from exceptions.chats import (
    ChatDataWebException,
    ChatListenerAddWebException,
    ChatListenerListWebException,
    ChatListWebException,
    ChatMessageCreateTimeoutRequestException,
    ChatMessageCreateWebException,
)
from httpx import AsyncClient, ConnectTimeout, HTTPStatusError
from services.constants import (
    CHAT_LIST_URI,
    CHAT_LISTENERS_URI,
    CHAT_MESSAGES_URI,
    CHAT_URI,
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
)
from services.converters.chats import convert_chat_listener_response_to_dto, convert_chat_response_to_dto


@dataclass
class BaseChatWebService(ABC):
    http_client: AsyncClient
    base_url: str

    @abstractmethod
    async def get_all_chats(self) -> list[ChatDTO]:
        pass

    @abstractmethod
    async def get_chat_listeners(self, chat_oid: str) -> list[ChatListenerDTO]:
        pass

    @abstractmethod
    async def add_listener(self, telegram_chat_id: str, chat_oid: str) -> None:
        pass

    @abstractmethod
    async def get_chat_data(self, chat_oid: str) -> ChatDTO:
        pass

    @abstractmethod
    async def create_message_in_chat(self, chat_oid: str, message_text: str):
        pass


@dataclass
class ChatWebService(BaseChatWebService):
    async def get_all_chats(self) -> list[ChatDTO]:
        response = await self.http_client.get(
            url=urljoin(base=self.base_url, url=CHAT_LIST_URI),
            params={"limit": DEFAULT_LIMIT, "offset": DEFAULT_OFFSET},
        )
        if not response.is_success:
            raise ChatListWebException(status_code=response.status_code, response_content=response.content.decode())
        json_data = response.json()
        return [convert_chat_response_to_dto(chat_data=chat_data) for chat_data in json_data["items"]]

    async def get_chat_listeners(self, chat_oid: str) -> list[ChatListenerDTO]:
        response = await self.http_client.get(
            url=urljoin(base=self.base_url, url=CHAT_LISTENERS_URI.format(chat_oid=chat_oid)),
        )
        if not response.is_success:
            raise ChatListenerListWebException(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )
        json_data = response.json()
        return [
            convert_chat_listener_response_to_dto(listener_data=listener_data) for listener_data in json_data["items"]
        ]

    async def add_listener(self, telegram_chat_id: str, chat_oid: str) -> None:
        response = await self.http_client.post(
            url=urljoin(base=self.base_url, url=CHAT_LISTENERS_URI.format(chat_oid=chat_oid)),
            json={"telegram_chat_id": telegram_chat_id},
        )
        if not response.is_success:
            raise ChatListenerAddWebException(
                response_content=response.content.decode(),
                status_code=response.status_code,
            )

    async def get_chat_data(self, chat_oid: str) -> ChatDTO:
        response = await self.http_client.get(
            url=urljoin(base=self.base_url, url=CHAT_URI.format(chat_oid=chat_oid)),
        )
        if not response.is_success:
            raise ChatDataWebException(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )
        json_data = response.json()
        return convert_chat_response_to_dto(chat_data=json_data)

    async def create_message_in_chat(self, chat_oid: str, message_text: str):
        try:
            response = await self.http_client.post(
                url=urljoin(base=self.base_url, url=CHAT_MESSAGES_URI.format(chat_oid=chat_oid)),
                json={"text": message_text},
            )
            response.raise_for_status()
        except HTTPStatusError as error:
            raise ChatMessageCreateWebException(
                response_content=error.response.content.decode(),
                status_code=error.response.status_code,
            )
        except ConnectTimeout:
            raise ChatMessageCreateTimeoutRequestException()
