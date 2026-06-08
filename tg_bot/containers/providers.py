from aiogram import Bot
from dishka import AnyOf, provide, Provider, Scope
from httpx import AsyncClient
from repositories.chats.base import BaseChatsRepository, SQLChatsRepository
from services.chats import ChatsService
from services.web import BaseChatWebService, ChatWebService

from settings.config import Config


class DefaultProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config()

    @provide(scope=Scope.REQUEST)
    def get_http_client(self) -> AsyncClient:
        return AsyncClient()

    @provide(scope=Scope.REQUEST)
    def get_chat_web_service(
        self,
        config: Config,
        http_client: AsyncClient,
    ) -> AnyOf[BaseChatWebService, ChatWebService]:
        return ChatWebService(http_client=http_client, base_url=config.web_api_base_url)

    @provide(scope=Scope.REQUEST)
    def get_telegram_bot(self, config: Config) -> Bot:
        return Bot(token=config.tg_bot_token)

    @provide(scope=Scope.REQUEST)
    def get_chats_repository(self, config: Config) -> AnyOf[BaseChatsRepository, SQLChatsRepository]:
        return SQLChatsRepository(database_url=config.database_name)

    @provide(scope=Scope.REQUEST)
    def get_chats_service(self, repository: BaseChatsRepository) -> ChatsService:
        return ChatsService(repository=repository)
