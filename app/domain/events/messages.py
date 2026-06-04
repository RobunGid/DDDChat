from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_oid: str
    message_text: str
    chat_oid: str
    title: ClassVar[str] = "New Message Received"


@dataclass
class NewChatCreatedEvent(BaseEvent):
    chat_oid: str
    chat_title: str
    title: ClassVar[str] = "New Chat Created"


@dataclass
class ChatDeletedEvent(BaseEvent):
    title: ClassVar[str] = "Chat was Deleted"
    chat_oid: str


@dataclass
class ListenerAddedEvent(BaseEvent):
    title: ClassVar[str] = "Chat Listener Added to Chat"
    listener_oid: str
