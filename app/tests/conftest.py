from punq import Container
from pytest import fixture

from infrastructure.repositories.messages.base import BaseChatsRepository
from logic.bus.base import ApplicationBus
from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture(scope="function")
def application_bus(container: Container) -> ApplicationBus:
    return container.resolve(ApplicationBus)


@fixture(scope="function")
def chat_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(BaseChatsRepository)
