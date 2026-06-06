from pydantic import BaseModel


class ChatMessageSchema(BaseModel):
    event_id: str
    occurred_at: str
    message_text: str
    message_oid: str
    chat_oid: str


class ChatSchema(BaseModel):
    chat_oid: str
    chat_title: str
