import curses


def load_logo():
    try:
        with open("ascii_logo.txt") as f:
            return [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        return ["[ ASCII LOGO MISSING ]"]


def draw_header(stdscr, logo_lines):
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(logo_lines):
        x = max(0, w // 2 - len(line) // 2)
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(i, x, line[: w - 1])
        stdscr.attroff(curses.color_pair(2))
    return len(logo_lines)


def draw_menu_list(stdscr, options, selected_idx, offset_y):
    h, w = stdscr.getmaxyx()
    for idx, item in enumerate(options):
        x = w // 2 - len(item) // 2
        y = offset_y + 2 + idx
        attr = curses.color_pair(1) if idx == selected_idx else curses.color_pair(2)
        stdscr.attron(attr)
        stdscr.addstr(y, x, item)
        stdscr.attroff(attr)


def get_input(stdscr, prompt, y, x):
    curses.echo()
    stdscr.addstr(y, x, prompt, curses.color_pair(2))
    stdscr.refresh()
    value = stdscr.getstr(y, x + len(prompt), 40).decode("utf-8")
    curses.noecho()
    return value
