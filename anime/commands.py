from collections.abc import Callable, Sequence
from dataclasses import dataclass
import os
import re
import shlex
from .menu_result import MenuResult

@dataclass(frozen=True)
class MenuContext:
    choices: Sequence[str]
    selected: int
    screen: str = "generic"
    targets: Sequence[str] | None = None

CommandHandler = Callable[[list[str], MenuContext], MenuResult | None]

@dataclass(frozen=True)
class Command:
    name: str
    handler: CommandHandler
    aliases: tuple[str, ...] = ()

def open_command(arguments, context):
    if not arguments:
        return None
    entry = " ".join(arguments)
    targets = context.targets if context.targets is not None else context.choices
    command = "open_anime" if context.screen == "episode" and context.targets is not None else "open"
    if entry.isdigit():
        selected = int(entry) - 1
        if 0 <= selected < len(targets):
            arguments = (targets[selected],) if command == "open_anime" else ()
            return MenuResult(selected=selected, command=command, arguments=arguments)
        return None
    for selected, choice in enumerate(targets):
        if choice.casefold() == entry.casefold():
            arguments = (choice,) if command == "open_anime" else ()
            return MenuResult(selected=selected, command=command, arguments=arguments)
    return None

def quit_command(arguments, _context):
    if arguments:
        return None
    command = "back" if _context.screen == "episode" else "quit"
    return MenuResult(command=command)

def episode_index(choices, episode):
    match = re.fullmatch(r"ep(\d+)", episode.casefold())
    if match is None:
        return None
    number = match.group(1)
    for index, choice in enumerate(choices):
        if re.match(rf"ep{number}(?:-|$)", choice, flags=re.IGNORECASE):
            return index
    return None

def first_unwatched_episode(choices):
    for index, choice in enumerate(choices):
        if re.match(r"ep\d+(?:-|$)", choice, flags=re.IGNORECASE) and not choice.endswith("watched"):
            return index
    return None

def play_command(arguments, context):
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
        targets = context.targets if context.targets is not None else context.choices
        for selected, choice in enumerate(targets):
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

def rename_command(arguments, context):
    if context.screen == "anime":
        if not arguments:
            return None
        anime_name = " ".join(arguments)
        targets = context.targets if context.targets is not None else context.choices
        for selected, choice in enumerate(targets):
            if choice.casefold() == anime_name.casefold():
                return MenuResult(
                    selected=selected,
                    command="rename_anime",
                    arguments=(choice,),
                )
        return None
    if context.screen == "episode":
        if not arguments:
            return MenuResult(command="rename_current")
        anime_name = " ".join(arguments)
        targets = context.targets if context.targets is not None else ()
        for selected, choice in enumerate(targets):
            if choice.casefold() == anime_name.casefold():
                return MenuResult(
                    selected=selected,
                    command="rename_anime",
                    arguments=(choice,),
                )
    return None

def add_command(arguments, context):
    if context.screen != "anime" or not arguments:
        return None
    return MenuResult(command="add_series", arguments=(" ".join(arguments),))

def move_command(arguments, context):
    """Build a move-series action from the anime-selection menu."""
    if context.screen != "anime" or not arguments:
        return None
    targets = context.targets if context.targets is not None else context.choices
    for split_at in range(len(arguments), 0, -1):
        series_name = " ".join(arguments[:split_at])
        for choice in targets:
            if choice.casefold() == series_name.casefold():
                destination = " ".join(arguments[split_at:])
                return MenuResult(
                    command="move_series",
                    arguments=(choice, destination) if destination else (choice,),
                )
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
    Command("rename", rename_command, aliases=("r",)),
    Command("add", add_command, aliases=("a",)),
    Command("move", move_command),
    Command("quit", quit_command, aliases=("q",)),
)

def run_command(command_line, context):
    try:
        parts = shlex.split(command_line, posix=os.name != "nt")
    except ValueError:
        return None
    if os.name == "nt":
        parts = [
            part[1:-1] if part[:1] in {"'", '"'} and part[-1:] == part[:1] else part
            for part in parts
        ]
    if not parts:
        return None
    command = COMMANDS.get(parts[0].casefold())
    if command is None:
        return None
    return command.handler(parts[1:], context)
