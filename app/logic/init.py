from functools import lru_cache

from punq import Container

from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator
from infrastructure.repositories.messages import BaseChatRepository, MemoryChatRepository
    
@lru_cache(1)
def init_container():
    container = Container()
    container.register(BaseChatRepository, MemoryChatRepository)
    container.register(CreateChatCommandHandler)
    
    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)]
        )
        return mediator
        
    container.register(Mediator, factory=init_mediator)
    return container