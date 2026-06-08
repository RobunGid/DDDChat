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
    chat_create_event_topic: str = Field(
        alias="CHAT_CREATE_EVENT_TOPIC",
    )
    chat_delete_event_topic: str = Field(
        alias="CHAT_DELETE_EVENT_TOPIC",
    )
    message_create_event_topic: str = Field(
        alias="MESSAGE_CREATE_EVENT_TOPIC",
    )
    kafka_url: str = Field(alias="KAFKA_URL")
