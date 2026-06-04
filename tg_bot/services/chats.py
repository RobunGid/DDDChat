from abc import ABC, abstractmethod
from dataclasses import dataclass

from motor.core import AgnosticClient


@dataclass
class BaseChatService(ABC):
    @abstractmethod
    async def set_current_chat(self, chat_oid: str, telegram_chat_id: str): ...


@dataclass
class BaseMongoDBService(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]
