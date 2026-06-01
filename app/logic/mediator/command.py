from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    Iterable,
)

from logic.commands.base import (
    BaseCommand,
    CommandHandler,
    CR,
    CT,
)


@dataclass(eq=False)
class CommandMediator(ABC, Generic[CT, CR]):
    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_command(
        self,
        command: CT,
        command_handlers: Iterable[CommandHandler[CT, CR]],
    ):
        self.commands_map[command].extend(command_handlers)

    @abstractmethod
    async def handle_command(self, command: BaseCommand) -> Iterable[CR]: ...
