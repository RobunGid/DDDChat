from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from faker import Faker
from httpx import Response

from application.api.messages.schemas import CreateChatResponseSchema


@pytest.mark.asyncio
async def test_create_message_fail_text_too_long(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
    chat: CreateChatResponseSchema,
):
    url = app.url_path_for("create_message_handler", chat_oid=chat.oid)
    text = faker.text(1024) + faker.text(1024)
    response: Response = client.post(url=url, json={"text": text})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT, response.json()

    json_data = response.json()
    assert json_data["detail"]["error"]


@pytest.mark.asyncio
async def test_create_message_fail_text_empty(app: FastAPI, client: TestClient, chat: CreateChatResponseSchema):
    url = app.url_path_for("create_message_handler", chat_oid=chat.oid)
    response: Response = client.post(url=url, json={"text": ""})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT, response.json()

    json_data = response.json()
    assert json_data["detail"]["error"]
