from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    tg_bot_token: str = Field(alias="TG_BOT_TOKEN")
    web_api_base_url: str = Field(alias="WEB_API_BASE_URL")

    kafka_url: str = Field(alias="KAFKA_URL")
    kafka_group_id: str = Field(alias="KAFKA_GROUP_ID")

    chat_create_event_topic: str = Field(
        alias="CHAT_CREATE_EVENT_TOPIC",
    )
    chat_delete_event_topic: str = Field(
        alias="CHAT_DELETE_EVENT_TOPIC",
    )
    message_create_event_topic: str = Field(
        alias="MESSAGE_CREATE_EVENT_TOPIC",
    )
    telegram_support_group_id: str = Field(
        alias="TELEGRAM_SUPPORT_GROUP_ID",
    )
    database_name: str = Field(alias="DATABASE_NAME")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(1)
def get_config() -> Config:
    return Config()
