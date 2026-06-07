from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    tg_bot_token: str = Field(alias="TG_BOT_TOKEN")
    web_api_base_url: str = Field(alias="WEB_API_BASE_URL")

    kafka_url: str = Field(alias="KAFKA_URL")
    kafka_group_id: str = Field(alias="KAFKA_GROUP_ID", default="tg-bot")

    new_message_received_event_topic: str = Field(
        default="new-messages",
        alias="NEW_MESSAGE_RECEIVED_EVENT_TOPIC",
    )
    new_chats_event_topic: str = Field(
        default="new-chats-topic",
        alias="NEW_CHATS_EVENT_TOPIC",
    )
    telegram_support_group_id: str = Field(
        alias="TELEGRAM_SUPPORT_GROUP_ID",
    )
    database_name: str = Field(alias="DATABASE_NAME")
    # TODO: standartize all topics, aliases
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(1)
def get_config() -> Config:
    return Config()
