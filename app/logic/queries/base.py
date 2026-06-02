from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)


@dataclass(frozen=True)
class BaseQuery(ABC):
    pass


QT = TypeVar("QT", bound=BaseQuery)  # Query Type
QR = TypeVar("QR", bound=Any)  # Query Result


@dataclass(frozen=True)
class BaseQueryHandler(ABC, Generic[QT, QR]):
    @abstractmethod
    async def handle(self, query: QT) -> QR:
        pass
