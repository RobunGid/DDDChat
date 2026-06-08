from dataclasses import dataclass

from domain.exceptions.base import ApplicationConflictException, ApplicationNotFoundException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(ApplicationConflictException):
    title: str

    @property
    def message(self):
        return f'Chat with title "{self.title}" already exists'


@dataclass(eq=False)
class ChatNotFoundException(ApplicationNotFoundException):
    chat_oid: str

    @property
    def message(self):
        return f'Chat with oid "{self.chat_oid}" not found'
