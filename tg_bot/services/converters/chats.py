from datetime import datetime

from dtos.chats import ChatDTO


def convert_chat_response_to_dto(chat: dict) -> ChatDTO:
    return ChatDTO(
        oid=chat["oid"],
        title=chat["title"],
        created_at=datetime.fromisoformat(chat["created_at"]),
    )
