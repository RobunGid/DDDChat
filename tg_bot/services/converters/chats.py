from datetime import datetime

from dtos.chats import ChatDTO


def convert_chat_response_to_dto(chat_data: dict) -> ChatDTO:
    return ChatDTO(
        oid=chat_data["oid"],
        title=chat_data["title"],
        created_at=datetime.fromisoformat(chat_data["created_at"]),
    )
