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
async def test_create_chat_success(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for("create_chat_handler")
    title = faker.text(max_nb_chars=30)
    response = client.post(url=url, json={"title": title})

    assert response.is_success

    json_data = response.json()
    assert json_data["title"] == title


@pytest.mark.asyncio
async def test_create_chat_fail_title_too_long(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for("create_chat_handler")
    title = faker.text(255) + faker.text(255)
    response: Response = client.post(url=url, json={"title": title})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT, response.json()

    json_data = response.json()
    assert json_data["detail"]["error"]


@pytest.mark.asyncio
async def test_create_chat_fail_title_empty(
    app: FastAPI,
    client: TestClient,
):
    url = app.url_path_for("create_chat_handler")
    response: Response = client.post(url=url, json={"title": ""})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT, response.json()

    json_data = response.json()
    assert json_data["detail"]["error"]


@pytest.mark.asyncio
async def test_delete_chat_success(app: FastAPI, client: TestClient, chat: CreateChatResponseSchema):
    url = app.url_path_for("delete_chat_handler", chat_oid=chat.oid)
    response = client.delete(url=url)

    assert response.is_success
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_chat_fail_not_found(app: FastAPI, client: TestClient, chat: CreateChatResponseSchema):
    url = app.url_path_for("delete_chat_handler", chat_oid=chat.oid)
    response_first = client.delete(url=url)
    response_second = client.delete(url=url)

    assert response_first.is_success
    assert response_first.status_code == 204

    assert not response_second.is_success
    assert response_second.status_code == 404


@pytest.mark.asyncio
async def test_get_chats_success(app: FastAPI, client: TestClient, chat: CreateChatResponseSchema):
    url = app.url_path_for("get_chats_handler")
    response = client.get(url=url)
    json_data = response.json()

    assert response.is_success
    assert response.status_code == 200
    assert json_data["count"] == 1
    assert json_data["items"][0]["oid"] == chat.oid
