from abc import ABC, abstractmethod
from dataclasses import dataclass

from infrastructure.integrations.notifications.dtos import Notification


@dataclass
class BaseNotificationClient(ABC):
    # TODO: BaseFormatter!!
    @abstractmethod
    async def _format_notification(self, notification: Notification) -> str:
        pass

    @abstractmethod
    async def send(self, notification: Notification):
        pass
