from dataclasses import dataclass

from domain.exceptions.base import ApplicationValidationException


@dataclass(eq=False)
class MessageTextEmptyException(ApplicationValidationException):
    @property
    def message(self):
        return "Message text is required but was not provided or is empty"


@dataclass(eq=False)
class MessageTextTooLongException(ApplicationValidationException):
    text: str

    @property
    def message(self):
        return f"Message text length exceeds allowed limit; received text starts with: {self.text[:255]}..."
