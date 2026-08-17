from dataclasses import dataclass

@dataclass
class MenuResult:
    selected: int | None = None
    command: str | None = None
    arguments: tuple[str, ...] = ()

    @property
    def is_command(self):
        return self.command is not None
