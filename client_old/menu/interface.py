import curses
from functools import wraps
from typing import Any, Callable, List, Union


def get_input(stdscr: curses.window, prompt: str, y: int, x: int) -> str:
    curses.echo()
    stdscr.addstr(y, x, prompt, curses.color_pair(2))
    stdscr.refresh()
    s = stdscr.getstr(y, x + len(prompt), 40).decode("utf-8")
    curses.noecho()
    return s


def load_header(path: str) -> List[str]:
    try:
        with open(path) as f:
            return [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        return ["[ ASCII HEADER MISSING ]"]


def draw_text(
    stdscr: curses.window,
    text: str,
    y: int,
    color_pair: int = 0,
    block_width: int | None = None,
) -> None:
    _, w = stdscr.getmaxyx()
    x = max(0, (w - (block_width or len(text))) // 2)
    stdscr.attron(curses.color_pair(color_pair))
    stdscr.addstr(y, x, text[: w - 1])
    stdscr.attroff(curses.color_pair(color_pair))


def draw_header(stdscr: curses.window, header: List[str]) -> None:
    for i, line in enumerate(header):
        draw_text(stdscr, line, i, 2)


def draw_menu_list(
    stdscr: curses.window, options: List[str], selected_idx: int, offset_y: int
) -> None:
    w = max(len(o) for o in options) if options else 0
    for idx, item in enumerate(options):
        draw_text(
            stdscr,
            item,
            offset_y + 2 + idx,
            1 if idx == selected_idx else 2,
            block_width=w,
        )


def get_navigation(
    stdscr: curses.window, menu_length: int, current_idx: int
) -> Union[int, None]:
    k = stdscr.getch()
    if k == -1:
        return None
    if k in (curses.KEY_UP, ord("k")) and current_idx > 0:
        return current_idx - 1
    if k in (curses.KEY_DOWN, ord("j")) and current_idx < menu_length - 1:
        return current_idx + 1
    if k in (curses.KEY_ENTER, ord("\n")):
        return -1
    if k == 27:
        return -2
    return current_idx


def init_colors() -> None:
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)


def menu_interface(
    header_path: str, choices: List[str] | None = None, *, refresh_ms: int | None = None
) -> Callable:
    choices = choices or []

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapped(stdscr: curses.window, *args: Any, **kwargs: Any) -> Any:
            init_colors()
            header = load_header(header_path)
            curses.curs_set(0)
            if refresh_ms is not None:
                stdscr.timeout(refresh_ms)
            current_idx = 0
            information_src: Union[List[str], Callable[[], List[str]]] = kwargs.pop(
                "information", []
            )

            def draw_screen() -> None:
                stdscr.clear()
                draw_header(stdscr, header)
                info_lines = (
                    information_src() if callable(information_src) else information_src
                )
                info_w = max((len(l) for l in info_lines), default=0)
                for i, line in enumerate(info_lines):
                    draw_text(stdscr, line, len(header) + 2 + i, block_width=info_w)
                offset = len(header) + max(1, len(info_lines)) + 2
                draw_menu_list(stdscr, choices, current_idx, offset)
                stdscr.refresh()

            while True:
                draw_screen()
                nav = get_navigation(stdscr, len(choices), current_idx)
                if nav is None:
                    continue
                if nav == -1:
                    result = func(
                        stdscr,
                        choices,
                        information_src,
                        current_idx,
                        header,
                        *args,
                        **kwargs,
                    )
                    if result == -2:
                        return -2
                    if result is not None:
                        return result
                elif nav == -2:
                    return -2
                else:
                    current_idx = nav

        return wrapped

    return decorator
