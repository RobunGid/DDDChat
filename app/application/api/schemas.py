
from typing import Generic, TypeVar

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    error: str
    
IT = TypeVar('IT', bound=BaseModel) # Items
    
class BaseQueryResponseSchema(BaseModel, Generic[IT]):
    count: int
    items: IT
    offset: int
    limit: int