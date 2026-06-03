from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    tg_bot_token: str = Field(alias="TG_BOT_TOKEN")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
