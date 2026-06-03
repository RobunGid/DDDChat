from abc import ABC, abstractmethod
from dataclasses import dataclass
from urllib.parse import urljoin

from dtos.messages import ChatListItemDTO
from exceptions.chats import ChatListRequestException
from httpx import AsyncClient
from services.constants import CHAT_LIST_URI, DEFAULT_LIMIT, DEFAULT_OFFSET
from services.converters.chats import convert_chat_response_to_dto


@dataclass
class BaseChatWebService(ABC):
    http_client: AsyncClient
    base_url: str

    @abstractmethod
    async def get_all_chats(self) -> list[ChatListItemDTO]:
        pass


@dataclass
class ChatWebService(BaseChatWebService):
    async def get_all_chats(self) -> list[ChatListItemDTO]:
        print(urljoin(base=self.base_url, url=CHAT_LIST_URI), 289348234)
        response = await self.http_client.get(
            url=urljoin(base=self.base_url, url=CHAT_LIST_URI),
            params={"limit": DEFAULT_LIMIT, "offset": DEFAULT_OFFSET},
        )
        if not response.is_success:
            raise ChatListRequestException(status_code=response.status_code, response_content=response.content.decode())
        json_data = response.json()
        return [convert_chat_response_to_dto(chat_data=chat_data) for chat_data in json_data["items"]]
