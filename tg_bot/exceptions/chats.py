import json
from dataclasses import dataclass

from exceptions.base import ApplicationException


@dataclass(eq=False)
class BaseWebException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def response_json(self) -> dict:
        return json.loads(self.response_content)

    @property
    def error_text(self) -> str:
        return self.response_json.get("detail", {}).get("error", "")


@dataclass(eq=False)
class ChatListWebException(BaseWebException):
    @property
    def message(self):
        return "Failed to retrieve list of chats"


@dataclass(eq=False)
class ChatListenerListWebException(BaseWebException):
    @property
    def message(self):
        return "Failed to retrieve list of chat listeners"


@dataclass(eq=False)
class ChatListenerAddWebException(BaseWebException):
    @property
    def message(self):
        return "Failed to add listener to chat"


@dataclass(eq=False)
class ChatAlreadyExistsException(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self):
        return "Chat with such data already exists"


@dataclass(eq=False)
class ChatDataNotFoundException(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self):
        return "Unable to find created chat"


@dataclass(eq=False)
class ChatDataWebException(BaseWebException):
    @property
    def message(self):
        return "Failed to retrieve chat information"


@dataclass(eq=False)
class ChatMessageCreateWebException(BaseWebException):
    @property
    def message(self):
        return "Failed to create message in chat"


@dataclass(eq=False)
class ChatMessageCreateTimeoutRequestException(ApplicationException):
    @property
    def message(self):
        return "Failed to created message in chat because of timeout"
