from dataclasses import dataclass

from domain.exceptions.chats import ChatTitleEmptyException, ChatTitleTooLongException
from domain.exceptions.messages import (
    MessageTextEmptyException,
    MessageTextTooLongException,
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject[str]):
    def validate(self):
        if not self.value:
            raise MessageTextEmptyException()
        if len(self.value) > 255:
            raise MessageTextTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject[str]):
    def validate(self):
        if not self.value:
            raise ChatTitleEmptyException()
        if len(self.value) > 255:
            raise ChatTitleTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)
