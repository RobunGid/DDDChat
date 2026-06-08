from datetime import datetime

from pydantic import BaseModel


class ChatDTO(BaseModel):
    oid: str
    title: str
    created_at: datetime

    def format_to_html(self) -> str:
        return f"💬 {self.title}\n🆔 <code>{self.oid}</code>\n📅 {self.created_at.strftime('%d.%m.%Y %H:%M')}"


class ChatDataDTO(BaseModel):
    telegram_chat_id: str
    web_chat_id: str
