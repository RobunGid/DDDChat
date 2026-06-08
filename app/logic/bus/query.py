from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)

from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
)


@dataclass(eq=False)
class QueryBus[QT: BaseQuery, QR](ABC):
    queries_map: dict[QT, BaseQueryHandler[QT, QR]] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(
        self,
        query: QT,
        query_handler: BaseQueryHandler[QT, QR],
    ) -> None:
        pass

    @abstractmethod
    async def handle_query(self, query: QT) -> QR:
        pass
