import curses
from curses import KEY_UP, KEY_DOWN, KEY_ENTER
from textwrap import wrap
import os
import shutil
from .kitty import show_image
from .constants import TERMINAL_NARROW

MENU_WIDTH = 55
IMAGE_X = 60
IMAGE_Y = 2

def kitty_available():
    return os.name != "nt" and shutil.which("kitty") is not None

def menu(stdscr, choices, items=None, picture=None):
    current = 0
    height, width = stdscr.getmaxyx()
    if width < MENU_WIDTH + 35:
        stdscr.addstr(
            0,
            0,
            TERMINAL_NARROW
        )
        stdscr.refresh()
        stdscr.getch()
        return 0
    win = curses.newwin(
        height,
        MENU_WIDTH,
        0,
        0
    )
    win.keypad(True)
    y = 0
    if items:
        for item in items:
            lines = wrap(str(item), MENU_WIDTH - 1)
            for line in lines:
                if y >= height - 1:
                    break
                win.addstr(
                    y,
                    0,
                    line[:MENU_WIDTH - 1]
                )
                y += 1
            if y >= height - 1:
                break
    y += 1
    menu_start = y
    for i, option in enumerate(choices):
        row = menu_start + i
        if row >= height:
            break
        text = (
            f"> {option}"
            if i == current
            else f"  {option}"
        )
        win.addstr(
            row,
            0,
            text[:MENU_WIDTH - 1]
        )
    win.refresh()
    if picture and kitty_available():
        show_image(
            picture,
            x=60,
            y=2,
        )
    while True:
        key = win.getch()
        if key == KEY_UP:
            old = current
            current = (current - 1) % len(choices)
        elif key == KEY_DOWN:
            old = current
            current = (current + 1) % len(choices)
        elif key in (KEY_ENTER, 10, 13):
            return current
        else:
            continue
        old_row = menu_start + old
        if old_row < height:
            win.addstr(
                old_row,
                0,
                f"  {choices[old]}"[:MENU_WIDTH - 1]
            )
        new_row = menu_start + current
        if new_row < height:
            win.addstr(
                new_row,
                0,
                f"> {choices[current]}"[:MENU_WIDTH - 1]
            )
        win.refresh()
