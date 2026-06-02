from pydantic import BaseModel

from infrastructure.repositories.filters.messages import (
    GetChatsFilters,
    GetMessagesFilters,
)


class GetMessagesFiltersSchema(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infrastructure(self):
        return GetMessagesFilters(
            limit=self.limit,
            offset=self.offset,
        )


class GetChatsFiltersSchema(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infrastructure(self):
        return GetChatsFilters(
            limit=self.limit,
            offset=self.offset,
        )
