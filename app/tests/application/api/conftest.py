from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest
from faker import Faker
from punq import Container

from application.api.main import create_app
from application.api.messages.schemas import CreateChatResponseSchema
from logic.init import init_container
from tests.fixtures import init_dummy_container


@pytest.fixture(scope="function")
def container():
    return init_dummy_container()


@pytest.fixture(scope="function")
def app(container: Container) -> FastAPI:
    app = create_app()
    app.dependency_overrides[init_container] = lambda: container
    return app


@pytest.fixture(scope="function")
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app, raise_server_exceptions=False)


@pytest.fixture(scope="function")
def chat(client: TestClient, app: FastAPI, faker: Faker) -> CreateChatResponseSchema:
    url = app.url_path_for("create_chat_handler")
    resp = client.post(url, json={"title": faker.text(100)})
    assert resp.status_code == 201
    return CreateChatResponseSchema.model_validate(resp.json())
