from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_oid: str
    message_text: str
    chat_oid: str
    title: ClassVar[str] = 'New Message Received'


@dataclass
class NewChatCreatedEvent(BaseEvent):
    chat_oid: str
    chat_title: str
    title: ClassVar[str] = 'New Chat Created'


@dataclass
class NewMessageReceivedFromBrokerEvent(BaseEvent):
    event_title: ClassVar[str] = 'New Message From Broker Received'

    message_text: str
    message_oid: str
    chat_oid: str
