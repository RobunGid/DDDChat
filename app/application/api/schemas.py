from typing import (
    Generic,
    Iterable,
    TypeVar,
)

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    error: str


IT = TypeVar("IT", bound=Iterable[BaseModel])  # Items


class BaseQueryResponseSchema(BaseModel, Generic[IT]):
    count: int
    items: IT
    offset: int
    limit: int
