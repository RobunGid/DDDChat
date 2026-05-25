import pytest
from faker import Faker
from datetime import datetime

from domain.events.messages import NewMessageReceivedEvent
from domain.values.messages import Text, Title
from domain.entities.messages import Chat, Message
from domain.exceptions.messages import TitleTooLongException

def test_create_message_success_short_text(faker: Faker):
    text = Text(faker.text(max_nb_chars=255))
    message = Message(text)
    
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()
    
def test_create_message_success_long_text(faker: Faker):
    text = Text(faker.text(255) + faker.text(255))
    message = Message(text)
    
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()
    
def test_create_chat_success(faker: Faker):
    title = Title(faker.text(max_nb_chars=255))
    chat = Chat(title=title)
    
    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()
    
def test_create_title_too_long(faker: Faker):
    with pytest.raises(TitleTooLongException):
        title = Title(faker.text(255) + faker.text(255))
    
def test_add_chat_to_message(faker: Faker):
    text = Text(faker.text(max_nb_chars=255))
    message = Message(text)
    
    title = Title(faker.text(max_nb_chars=255))
    chat = Chat(title=title)
    
    chat.add_message(message)
    
    assert message in chat.messages
    
def test_new_message_events(faker: Faker):
    text = Text(faker.text(max_nb_chars=255))
    message = Message(text)
    
    title = Title(faker.text(max_nb_chars=255))
    chat = Chat(title=title)
    
    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()
    
    assert not pulled_events, pulled_events
    assert len(events) == 1, events
    
    new_event = events[0]
    
    assert isinstance(new_event, NewMessageReceivedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_oid == chat.oid