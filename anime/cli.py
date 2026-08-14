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
    offset = 0
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
    visible = height - menu_start
    if visible <= 0:
        return 0
    def draw_menu():
        win.erase()
        y = 0
        if items:
            for item in items:
                lines = wrap(str(item), MENU_WIDTH - 1)
                for line in lines:
                    if y >= menu_start:
                        break
                    win.addstr(
                        y,
                        0,
                        line[:MENU_WIDTH - 1]
                    )
                    y += 1
                if y >= menu_start:
                    break
        for row in range(visible):
            index = offset + row
            if index >= len(choices):
                break
            text = (
                f"> {choices[index]}"
                if index == current
                else f"  {choices[index]}"
            )
            win.addstr(
                menu_start + row,
                0,
                text[:MENU_WIDTH - 1]
            )
        win.refresh()
    draw_menu()
    if picture and kitty_available():
        show_image(
            picture,
            x=IMAGE_X,
            y=IMAGE_Y,
        )
    while True:
        key = win.getch()
        if key == KEY_UP:
            current = (current - 1) % len(choices)
        elif key == KEY_DOWN:
            current = (current + 1) % len(choices)
        elif key in (KEY_ENTER, 10, 13):
            return current
        else:
            continue
        if current >= offset + visible:
            offset = current - visible + 1
        elif current < offset:
            offset = current
        draw_menu()
