from dataclasses import dataclass
from urllib.parse import urljoin

from dtos.chats import ChatDTO
from exceptions.chats import (
    ChatListWebException,
    ChatMessageCreateTimeoutWebException,
    ChatMessageCreateWebException,
    ChatWebException,
)
from httpx import ConnectTimeout, HTTPStatusError

from services.base import BaseChatWebService
from services.constants import (
    CHAT_LIST_URI,
    CHAT_MESSAGES_URI,
    CHAT_URI,
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
)
from services.converters.chats import convert_chat_response_to_dto


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
        return [convert_chat_response_to_dto(chat=chat) for chat in json_data["items"]]

    async def get_chat(self, chat_oid: str) -> ChatDTO:
        response = await self.http_client.get(
            url=urljoin(base=self.base_url, url=CHAT_URI.format(chat_oid=chat_oid)),
        )
        if not response.is_success:
            raise ChatWebException(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )
        json_data = response.json()
        return convert_chat_response_to_dto(chat=json_data)

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
            raise ChatMessageCreateTimeoutWebException()
