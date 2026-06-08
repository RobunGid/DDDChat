from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(alias="MONGO_DB_CONNECTION_URI")
    mongodb_chat_database: str = Field(alias="MONGO_DB_CHAT_DATABASE")
    mongodb_chat_collection: str = Field(
        alias="MONGO_DB_CHAT_COLLECTION",
    )
    mongodb_messages_collection: str = Field(
        alias="MONGO_DB_MESSAGES_COLLECTION",
    )
    new_chats_event_topic: str = Field(
        alias="NEW_CHATS_EVENT_TOPIC",
    )
    chats_deleted_event_topic: str = Field(
        alias="CHATS_DELETED_EVENT_TOPIC",
    )
    new_message_received_event_topic: str = Field(
        alias="NEW_MESSAGE_RECEIVED_EVENT_TOPIC",
    )
    kafka_url: str = Field(alias="KAFKA_URL")
