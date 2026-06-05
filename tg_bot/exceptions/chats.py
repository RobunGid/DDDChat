from attr import dataclass
from exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class ChatListRequestException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def message(self):
        return "Could not get chats"


@dataclass(frozen=True, eq=False)
class ChatListeneListRequestException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def message(self):
        return "Could not get chat listeners"
