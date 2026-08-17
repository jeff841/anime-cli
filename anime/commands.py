from collections.abc import Callable, Sequence
from dataclasses import dataclass
import re
import shlex

from .menu_result import MenuResult


@dataclass(frozen=True)
class MenuContext:
    choices: Sequence[str]
    selected: int
    screen: str = "generic"


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


def episode_index(choices, episode):
    """Return the index for an episode such as ``ep12``."""
    match = re.fullmatch(r"ep(\d+)", episode.casefold())
    if match is None:
        return None
    number = match.group(1)
    for index, choice in enumerate(choices):
        if re.match(rf"ep{number}(?:-|$)", choice, flags=re.IGNORECASE):
            return index
    return None


def first_unwatched_episode(choices):
    """Return the first episode entry that has not received the watched suffix."""
    for index, choice in enumerate(choices):
        if re.match(r"ep\d+(?:-|$)", choice, flags=re.IGNORECASE) and not choice.endswith("watched"):
            return index
    return None


def play_command(arguments, context):
    """Build a play action appropriate for the menu that received the command."""
    if context.screen == "anime":
        if not arguments:
            return None

        episode = None
        if re.fullmatch(r"ep\d+", arguments[-1], flags=re.IGNORECASE):
            episode = arguments[-1]
            arguments = arguments[:-1]
        if not arguments:
            return None

        anime_name = " ".join(arguments)
        for selected, choice in enumerate(context.choices):
            if choice.casefold() == anime_name.casefold():
                return MenuResult(
                    selected=selected,
                    command="play",
                    arguments=(episode,) if episode else (),
                )
        return None

    if context.screen == "episode":
        if len(arguments) > 1:
            return None
        selected = (
            episode_index(context.choices, arguments[0])
            if arguments
            else first_unwatched_episode(context.choices)
        )
        if selected is None:
            return None
        return MenuResult(selected=selected, command="play")

    return None


def command_registry(*commands):
    return {
        alias.casefold(): command
        for command in commands
        for alias in (command.name, *command.aliases)
    }


COMMANDS = command_registry(
    Command("open", open_command, aliases=("o",)),
    Command("play", play_command, aliases=("p",)),
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
