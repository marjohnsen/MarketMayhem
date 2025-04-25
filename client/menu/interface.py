import curses
from functools import wraps
from typing import List, Callable, Any


def load_header(path: str) -> List[str]:
    try:
        with open(path) as f:
            return [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        return ["[ ASCII HEADER MISSING ]"]


def draw_centered_text(
    stdscr: curses.window, text: str, y: int, color_pair: int = 0
) -> None:
    _, w = stdscr.getmaxyx()
    x = max(0, w // 2 - len(text) // 2)
    stdscr.attron(curses.color_pair(color_pair))
    stdscr.addstr(y, x, text[: w - 1])
    stdscr.attroff(curses.color_pair(color_pair))


def draw_header(stdscr: curses.window, header: List[str]) -> None:
    for i, line in enumerate(header):
        draw_centered_text(stdscr, line, i, 2)


def draw_menu_list(
    stdscr: curses.window, options: List[str], selected_idx: int, offset_y: int
) -> None:
    for idx, item in enumerate(options):
        attr = 1 if idx == selected_idx else 2
        draw_centered_text(stdscr, item, offset_y + 2 + idx, attr)


def get_input(stdscr: curses.window, prompt: str, y: int, x: int) -> str:
    curses.echo()
    stdscr.addstr(y, x, prompt, curses.color_pair(2))
    stdscr.refresh()
    input_str = stdscr.getstr(y, x + len(prompt), 40).decode("utf-8")
    curses.noecho()
    return input_str


def get_navigation(stdscr: curses.window, menu_length: int, current_idx: int) -> int:
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


def init_colors() -> None:
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)


def menu_interface(header_path: str, choices: List[str] = None) -> Callable:
    choices = choices or []

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapped(stdscr: curses.window, *args: Any, **kwargs: Any) -> None:
            init_colors()
            header = load_header(header_path)
            curses.curs_set(0)
            current_idx = 0

            information = kwargs.pop("information", [])

            def draw_screen() -> Any:
                stdscr.clear()
                draw_header(stdscr, header)

                for i, line in enumerate(information):
                    draw_centered_text(stdscr, line, len(header) + 2 + i)
                offset = len(header) + max(1, len(information)) + 2
                draw_menu_list(stdscr, choices, current_idx, offset)
                stdscr.refresh()

            while True:
                draw_screen()
                nav = get_navigation(stdscr, len(choices), current_idx)

                if nav == -1:
                    if (
                        func(
                            stdscr,
                            choices,
                            information,
                            current_idx,
                            header,
                            len(header) + len(information) + 2,
                            *args,
                            **kwargs,
                        )
                        == -2
                    ):
                        break
                    draw_screen()
                elif nav == -2:
                    break
                else:
                    current_idx = nav

            return -2

        return wrapped

    return decorator
