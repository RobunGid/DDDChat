from dataclasses import dataclass

from domain.exceptions.base import ApplicationValidationException


@dataclass(eq=False)
class ChatTitleEmptyException(ApplicationValidationException):
    @property
    def message(self):
        return "Chat title is required but was not provided or is empty"


@dataclass(eq=False)
class ChatTitleTooLongException(ApplicationValidationException):
    text: str

    @property
    def message(self):
        return f"Chat title length exceeds allowed limit; received text starts with: {self.text[:255]}..."
