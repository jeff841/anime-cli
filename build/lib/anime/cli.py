from curses import wrapper,KEY_UP,KEY_DOWN,KEY_ENTER

def menu(stdscr,choices):
    current = 0

    while True:
        stdscr.clear()
        for i,option in enumerate(choices):
            if i == current:
                stdscr.addstr(i,0,f'> {option}')
            else:
                stdscr.addstr(i,0,f'  {option}')
        key = stdscr.getch()
        if key == KEY_UP:
            current = (current - 1) % len(choices)
        elif key == KEY_DOWN:
            current = (current + 1) % len(choices)
        elif key == KEY_ENTER or key in [10,13]:
            return current

