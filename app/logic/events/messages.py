from dataclasses import dataclass

from domain.events.messages import NewChatCreatedEvent, NewMessageReceivedEvent
from logic.events.base import EventHandler
from infrastructure.message_brokers.converters import convert_event_to_broker_message


@dataclass
class NewChatCreatedEventHandler(EventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> None:
        await self.message_broker.send_message(
			topic=self.broker_topic,
			value=convert_event_to_broker_message(event=event),
   			key=str(event.event_id).encode()
		)
        
@dataclass
class NewMessageReceivedEventHandler(EventHandler[NewMessageReceivedEvent, None]):
    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.message_broker.send_message(
			topic=self.broker_topic,
			value=convert_event_to_broker_message(event=event),
   			key=str(event.event_id).encode()
		)