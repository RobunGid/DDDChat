from dataclasses import dataclass, field

from domain.values.messages import Text, Title
from domain.entities.base import BaseEntity

@dataclass(eq=False)
class Message(BaseEntity):
    text: Text
    
@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(default_factory=set, kw_only=True)
    
    def add_message(self, message: Message):
        self.messages.add(message)