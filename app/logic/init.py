from functools import lru_cache
from uuid import uuid4

from aiojobs import Scheduler
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from domain.events.messages import (
    ChatDeletedEvent,
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.kafka import KafkaMessageBroker
from infrastructure.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from infrastructure.repositories.messages.mongodb import (
    MongoDBChatsRepository,
    MongoDBMessagesRepository,
)
from infrastructure.websockets.managers import (
    BaseConnectionManager,
    ConnectionManager,
)
from logic.bus.base import ApplicationBus
from logic.bus.event import EventBus
from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
    DeleteChatCommand,
    DeleteChatCommandHandler,
)
from logic.events.messages import (
    ChatDeletedEventHandler,
    NewChatCreatedEventHandler,
    NewMessageReceivedEventHandler,
    NewMessageReceivedFromBrokerEvent,
    NewMessageReceivedFromBrokerEventHandler,
)
from logic.queries.messages import (
    GetChatQuery,
    GetChatQueryHandler,
    GetChatsQuery,
    GetChatsQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)
from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.mongodb_connection_uri,
            serverSelectionTimeoutMS=3000,
        )

    container.register(
        AsyncIOMotorClient,
        factory=create_mongodb_client,
        scope=Scope.singleton,
    )
    client = container.resolve(AsyncIOMotorClient)

    def init_chats_mongodb_repository() -> MongoDBChatsRepository:
        return MongoDBChatsRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    def init_messages_mongodb_repository() -> MongoDBMessagesRepository:
        return MongoDBMessagesRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_messages_collection,
        )

    container.register(
        BaseChatsRepository,
        factory=init_chats_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseMessagesRepository,
        factory=init_messages_mongodb_repository,
        scope=Scope.singleton,
    )
    # Command Handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    # Query Handler
    container.register(GetChatQueryHandler)
    container.register(GetMessagesQueryHandler)
    container.register(GetChatsQueryHandler)

    def init_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.kafka_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.kafka_url,
                group_id=f"chats-{uuid4()}",
                metadata_max_age_ms=30000,
            ),
        )

    container.register(
        BaseMessageBroker,
        factory=init_message_broker,
        scope=Scope.singleton,
    )

    def init_application_bus() -> ApplicationBus:
        application_bus = ApplicationBus()

        # Message handlers
        create_chat_handler = CreateChatCommandHandler(
            _command_bus=application_bus,
            chats_repository=container.resolve(BaseChatsRepository),
        )
        delete_chat_handler = DeleteChatCommandHandler(
            _command_bus=application_bus,
            chats_repository=container.resolve(BaseChatsRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _command_bus=application_bus,
            messages_repository=container.resolve(BaseMessagesRepository),
            chats_repository=container.resolve(BaseChatsRepository),
        )
        # Event handlers
        chat_create_event_handler = NewChatCreatedEventHandler(
            broker_topic=config.chat_create_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
        )
        message_create_event_handler = NewMessageReceivedEventHandler(
            broker_topic=config.message_create_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
        )
        new_message_received_from_broker_event_handler = NewMessageReceivedFromBrokerEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            broker_topic=config.message_create_event_topic,
            connection_manager=container.resolve(BaseConnectionManager),
        )
        chat_delete_event_handler = ChatDeletedEventHandler(
            broker_topic=config.chat_delete_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
        )
        # Events
        application_bus.register_event(
            NewChatCreatedEvent,
            [chat_create_event_handler],
        )
        application_bus.register_event(
            NewMessageReceivedEvent,
            [message_create_event_handler],
        )
        application_bus.register_event(
            NewMessageReceivedFromBrokerEvent,
            [new_message_received_from_broker_event_handler],
        )
        application_bus.register_event(
            ChatDeletedEvent,
            [chat_delete_event_handler],
        )
        # Commands
        application_bus.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )
        application_bus.register_command(
            DeleteChatCommand,
            [delete_chat_handler],
        )
        application_bus.register_command(
            CreateMessageCommand,
            [create_message_handler],
        )
        # Queries
        application_bus.register_query(
            GetChatQuery,
            container.resolve(GetChatQueryHandler),
        )
        application_bus.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )
        application_bus.register_query(
            GetChatsQuery,
            container.resolve(GetChatsQueryHandler),
        )
        return application_bus

    container.register(ApplicationBus, factory=init_application_bus)
    container.register(EventBus, factory=init_application_bus)
    container.register(
        BaseConnectionManager,
        instance=ConnectionManager(),
        scope=Scope.singleton,
    )

    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container
