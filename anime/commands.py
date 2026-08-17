from collections.abc import Callable, Sequence
from dataclasses import dataclass
import shlex

from .menu_result import MenuResult


@dataclass(frozen=True)
class MenuContext:
    choices: Sequence[str]
    selected: int


CommandHandler = Callable[[list[str], MenuContext], MenuResult | None]


@dataclass(frozen=True)
class Command:
    name: str
    handler: CommandHandler
    aliases: tuple[str, ...] = ()


def open_command(arguments, context):
    """Open a menu entry identified by its one-based number or exact name."""
    if not arguments:
        return None

    entry = " ".join(arguments)
    if entry.isdigit():
        selected = int(entry) - 1
        if 0 <= selected < len(context.choices):
            return MenuResult(selected=selected, command="open")
        return None

    for selected, choice in enumerate(context.choices):
        if choice.casefold() == entry.casefold():
            return MenuResult(selected=selected, command="open")
    return None


def quit_command(arguments, _context):
    """Exit the application."""
    if arguments:
        return None
    return MenuResult(command="quit")


def command_registry(*commands):
    return {
        alias.casefold(): command
        for command in commands
        for alias in (command.name, *command.aliases)
    }


COMMANDS = command_registry(
    Command("open", open_command, aliases=("o",)),
    Command("quit", quit_command, aliases=("q",)),
)


def run_command(command_line, context):
    """Parse and dispatch a command-line entry through the command registry."""
    try:
        parts = shlex.split(command_line)
    except ValueError:
        return None
    if not parts:
        return None

    command = COMMANDS.get(parts[0].casefold())
    if command is None:
        return None
    return command.handler(parts[1:], context)
