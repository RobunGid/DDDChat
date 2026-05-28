from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

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
from logic.mediator import Mediator
from infrastructure.repositories.messages.base import (
    BaseChatsRepository, 
    BaseMessagesRepository
)
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
    
    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)]
        )
        mediator.register_command(
            CreateMessageCommand,
            [container.resolve(CreateMessageCommandHandler)]
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
    
    return container