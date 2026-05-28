

from datetime import datetime
from typing import Iterable

from pydantic import BaseModel

from domain.entities.messages import Chat, Message


class CreateChatRequestSchema(BaseModel):
    title: str
    
class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str
    
    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type()
        )
        
class CreateMessageRequestSchema(BaseModel):
    text: str
    
class CreateMessageResponseSchema(BaseModel):
    oid: str
    text: str
    
    @classmethod
    def from_entity(cls, message: Message) -> 'CreateMessageResponseSchema':
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type()
        )
    
class ResponseMessageSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime
    
    @classmethod
    def from_entity(cls, message: Message) -> 'ResponseMessageSchema':
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type(),
            created_at=message.created_at,
        )
        
class ResponseChatSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime
    
    @classmethod
    def from_entity(cls, chat: Chat) -> 'ResponseChatSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
        )