from dataclasses import dataclass

from exceptions.base import ApplicationException


@dataclass(eq=False)
class ChatListRequestException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def message(self):
        return "Could not get chats"


@dataclass(eq=False)
class ChatListenerListRequestException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def message(self):
        return "Could not get chat listeners"


@dataclass(eq=False)
class ListenerAddRequestException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def message(self):
        return "Could not add chat listener"


@dataclass(eq=False)
class ChatRequestException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def message(self):
        return "Could not get this chat"
