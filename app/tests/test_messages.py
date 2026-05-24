import pytest
from faker import Faker
from datetime import datetime

from domain.values.messages import Text, Title
from domain.entities.messages import Chat, Message
from domain.exceptions.messages import TitleTooLongException

fake = Faker()

def test_create_message_success_short_text():
    text = Text(fake.text(max_nb_chars=255))
    message = Message(text)
    
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()
    
def test_create_message_success_long_text():
    text = Text(fake.text(255) + fake.text(255))
    message = Message(text)
    
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()
    
def test_create_chat_success():
    title = Title(fake.text(max_nb_chars=255))
    chat = Chat(title=title)
    
    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()
    
def test_create_title_too_long():
    with pytest.raises(TitleTooLongException):
        title = Title(fake.text(255) + fake.text(255))
    
def test_add_chat_to_message():
    text = Text(fake.text(max_nb_chars=255))
    message = Message(text)
    
    title = Title(fake.text(max_nb_chars=255))
    chat = Chat(title=title)
    
    chat.add_message(message)
    
    assert message in chat.messages