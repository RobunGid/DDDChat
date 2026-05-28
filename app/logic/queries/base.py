from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


@dataclass(frozen=True)
class BaseQuery(ABC):
    ...
    
QT = TypeVar('CT', bound=BaseQuery) # Query Type
QR = TypeVar("CR", bound=Any) # Query Result
    
@dataclass(frozen=True)
class BaseQueryHandler(ABC, Generic[QT, QR]):
    @abstractmethod
    async def handle(self, query: QT) -> QR:
        ...
        