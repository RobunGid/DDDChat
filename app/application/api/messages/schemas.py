from datetime import datetime

from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.messages import (
    Chat,
    ChatListener,
    Message,
)


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> "CreateChatResponseSchema":
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )


class CreateMessageRequestSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    oid: str
    text: str

    @classmethod
    def from_entity(cls, message: Message) -> "CreateMessageResponseSchema":
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type(),
        )


class ResponseMessageSchema(BaseModel):
    oid: str
    chat_oid: str
    text: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> "ResponseMessageSchema":
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type(),
            created_at=message.created_at,
            chat_oid=message.chat_oid,
        )


class ResponseChatSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> "ResponseChatSchema":
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
        )


class GetMessagesQueryResponseSchema(
    BaseQueryResponseSchema[list[ResponseMessageSchema]],
):
    pass


class GetChatsQueryResponseSchema(BaseQueryResponseSchema[list[ResponseChatSchema]]):
    pass


class RequestAddTelegramListenerSchema(BaseModel):
    telegram_chat_id: str


class ResponseAddTelegramListenerSchema(BaseModel):
    listener_id: str

    @classmethod
    def from_entity(cls, chat_listener: ChatListener) -> "ResponseAddTelegramListenerSchema":
        return cls(listener_id=chat_listener.oid)


class ResponseListenerSchema(BaseModel):
    oid: str

    @classmethod
    def from_entity(cls, listener: ChatListener) -> "ResponseListenerSchema":
        return cls(
            oid=listener.oid,
        )


class GetListenersQueryResponseSchema(BaseQueryResponseSchema[list[ResponseListenerSchema]]):
    pass
