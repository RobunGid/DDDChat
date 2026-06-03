from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    tg_bot_token: str = Field(alias="TG_BOT_TOKEN")
    web_api_base_url: str = Field(alias="WEB_API_BASE_URL")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(1)
def get_config() -> Config:
    return Config()
