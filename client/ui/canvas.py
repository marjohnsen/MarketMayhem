import curses
from typing import Sequence


class Canvas:
    def __init__(self, stdscr, offset):
        self.stdscr = stdscr
        self.offset = offset
        self.build()

    def build(self):
        y_max, x_max = self.stdscr.getmaxyx()
        h = y_max - self.offset - 1
        w = x_max - 2
        self.win = curses.newwin(h, w, self.offset, 1)
        self.win.keypad(True)

    def rebuild(self):
        self.build()

    def draw_list(
        self, lines: Sequence[str], *, selected: int | None = None, pair: int = 0
    ):
        h, w = self.win.getmaxyx()
        base = curses.color_pair(pair)
        for i, text in enumerate(lines[: h - 2]):
            y = i + 1
            x = max(0, (w - len(text)) // 2)
            attr = base | (curses.A_REVERSE if i == selected else 0)
            self.win.addnstr(y, x, text, w - x - 1, attr)

    def __getattr__(self, name):
        return getattr(self.win, name)
