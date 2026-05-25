
from dataclasses import dataclass

from domain.events.base import BaseEvent

@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_oid: str
    message_text: str
    chat_oid: str