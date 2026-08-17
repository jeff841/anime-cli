from dataclasses import dataclass
from typing import Literal

@dataclass
class MenuResult:
    selected: int | None = None
    command: str | None = None

    @property
    def is_command(self):
        return self.command is not None
