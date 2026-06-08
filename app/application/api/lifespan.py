from infrastructure.message_brokers.base import BaseMessageBroker
from logic.bus.base import ApplicationBus
from logic.events.messages import NewMessageReceivedFromBrokerEvent
from logic.init import init_container
from settings.config import Config


async def init_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def close_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()


async def consumer_in_background():
    container = init_container()
    config = container.resolve(Config)
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    cqrs_bus = container.resolve(ApplicationBus)

    async for msg in message_broker.start_consuming(
        config.message_create_event_topic,
    ):
        await cqrs_bus.publish(
            [
                NewMessageReceivedFromBrokerEvent(
                    message_text=msg["message_text"],
                    message_oid=msg["message_oid"],
                    chat_oid=msg["chat_oid"],
                ),
            ],
        )
