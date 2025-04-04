import curses
from functools import wraps


def load_header(path):
    try:
        with open(path) as f:
            return [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        return ["[ ASCII HEADER MISSING ]"]


def draw_centered_text(stdscr, text, y, color_pair=0):
    _, w = stdscr.getmaxyx()
    x = max(0, w // 2 - len(text) // 2)
    stdscr.attron(curses.color_pair(color_pair))
    stdscr.addstr(y, x, text[: w - 1])
    stdscr.attroff(curses.color_pair(color_pair))


def draw_header(stdscr, header):
    for i, line in enumerate(header):
        draw_centered_text(stdscr, line, i, 2)


def draw_menu_list(stdscr, options, selected_idx, offset_y):
    for idx, item in enumerate(options):
        attr = 1 if idx == selected_idx else 2
        draw_centered_text(stdscr, item, offset_y + 2 + idx, attr)


def get_input(stdscr, prompt, y, x):
    curses.echo()
    stdscr.addstr(y, x, prompt, curses.color_pair(2))
    stdscr.refresh()
    input = stdscr.getstr(y, x + len(prompt), 40).decode("utf-8")
    curses.noecho()
    return input


def get_navigation(stdscr, menu_length, current_idx):
    key = stdscr.getch()
    if key in (curses.KEY_UP, ord("k")) and current_idx > 0:
        return current_idx - 1
    elif key in (curses.KEY_DOWN, ord("j")) and current_idx < menu_length - 1:
        return current_idx + 1
    elif key in (curses.KEY_ENTER, ord("\n")):
        return -1  # Select
    elif key == 27:
        return -2  # Exit
    return current_idx


def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)


def menu_interface(header_path, options=[]):
    def decorator(func):
        @wraps(func)
        def wrapped(stdscr, *args, **kwargs):
            init_colors()
            header = load_header(header_path)
            offset = len(header)
            curses.curs_set(0)
            current_idx = 0

            def draw_screen():
                stdscr.clear()
                draw_header(stdscr, header)
                draw_menu_list(stdscr, options, current_idx, offset)
                stdscr.refresh()

            if not options:
                draw_screen()
                func(stdscr, options, current_idx, header, offset, *args, **kwargs)
                return

            while True:
                draw_screen()
                idx = get_navigation(stdscr, len(options), current_idx)

                if idx == -1:
                    if (
                        func(
                            stdscr,
                            options,
                            current_idx,
                            header,
                            offset,
                            *args,
                            **kwargs,
                        )
                        == -2
                    ):
                        break
                elif idx == -2:
                    break
                else:
                    current_idx = idx

        return wrapped

    return decorator
