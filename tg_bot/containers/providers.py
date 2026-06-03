from dishka import provide, Provider, Scope
from httpx import AsyncClient
from services.web import BaseChatWebService, ChatWebService

from settings.config import Config


class DefaultProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config()

    @provide(scope=Scope.REQUEST)
    def get_http_client(self) -> AsyncClient:
        return AsyncClient()

    @provide(scope=Scope.APP)
    def get_chat_web_service(self) -> BaseChatWebService:
        return ChatWebService(http_client=self.get_http_client(), base_url=self.get_config().web_api_base_url)
