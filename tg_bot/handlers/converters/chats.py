from aiogram_i18n import I18nContext
from dtos.messages import ChatDTO


def convert_chat_dtos_to_translated_message(
    chats: list[ChatDTO],
    i18n: I18nContext,
) -> str:
    return "\n\n".join(
        i18n.get(
            "chat_list_item",
            number=i + 1,
            title=chat.title,
            oid=chat.oid,
            created_at=chat.created_at,
        )
        for i, chat in enumerate(chats)
    )
