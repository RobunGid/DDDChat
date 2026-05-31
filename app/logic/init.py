from functools import lru_cache

from aiokafka import AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from domain.events.messages import NewChatCreatedEvent, NewMessageReceivedEvent
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.kafka import KafkaMessageBroker
from infrastructure.repositories.messages.mongodb import (
    MongoDBChatsRepository, 
    MongoDBMessagesRepository
)
from logic.commands.messages import (
    CreateChatCommand, 
    CreateChatCommandHandler, 
    CreateMessageCommand, 
    CreateMessageCommandHandler
)
from logic.events.messages import NewChatCreatedEventHandler, NewMessageReceivedEventHandler
from logic.mediator.base import Mediator
from infrastructure.repositories.messages.base import (
    BaseChatsRepository, 
    BaseMessagesRepository
)
from logic.mediator.event import EventMediator
from logic.queries.messages import GetChatQuery, GetChatQueryHandler, GetMessagesQuery, GetMessagesQueryHandler
from settings.config import Config
    
@lru_cache(1)
def init_container() -> Container:
    return _init_container()

def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)
    
    def create_mongodb_client():
        return AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
    
    container.register(AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton)
    client = container.resolve(AsyncIOMotorClient)
    
    def init_chats_mongodb_repository() -> MongoDBChatsRepository:
        return MongoDBChatsRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection
        )
        
    def init_messages_mongodb_repository() -> MongoDBMessagesRepository:
        return MongoDBMessagesRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_messages_collection
        )
        
        
    container.register(BaseChatsRepository, factory=init_chats_mongodb_repository, scope=Scope.singleton)
    container.register(BaseMessagesRepository, factory=init_messages_mongodb_repository, scope=Scope.singleton)
    
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)
    
    container.register(GetChatQueryHandler)
    container.register(GetMessagesQueryHandler)
    
    def init_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
			producer=AIOKafkaProducer(bootstrap_servers=config.kafka_url)
		)
    
    container.register(BaseMessageBroker, factory=init_message_broker, scope=Scope.singleton)
    
    def init_mediator() -> Mediator:
        mediator = Mediator()
        
        # Message handlers
        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
			chats_repository=container.resolve(BaseChatsRepository)
   		)
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
			messages_repository=container.resolve(BaseMessagesRepository),
			chats_repository=container.resolve(BaseChatsRepository)
   		)
        
        # Event handlers
        new_chat_created_event_handler = NewChatCreatedEventHandler(
			broker_topic=config.new_chats_event_topic,
			message_broker=container.resolve(BaseMessageBroker)
		)
        new_message_received_event_handler = NewMessageReceivedEventHandler(
			broker_topic=config.new_message_received_event_topic,
			message_broker=container.resolve(BaseMessageBroker)
		)
        mediator.register_event(
			NewChatCreatedEvent,
			[new_chat_created_event_handler]
		)
        mediator.register_event(
			NewMessageReceivedEvent,
			[new_message_received_event_handler]
		)
        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler]
        )
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler]
        )
        mediator.register_query(
            GetChatQuery,
            container.resolve(GetChatQueryHandler)
        )
        mediator.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler)
        )
        return mediator
    
    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)
    
    return container