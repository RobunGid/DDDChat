
from domain.entities.messages import Chat, Message

def convert_message_entity_to_document(message: Message) -> dict:
    return {
		'oid': message.oid,
		'created_at': message.created_at,
		'text': message.text.as_generic_type(),
	}

def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
		'oid': chat.oid,
  		'title': chat.title.as_generic_type(),
		'messages': [convert_message_entity_to_document(message) for message in chat.messages],
		'created_at': chat.created_at,
	}