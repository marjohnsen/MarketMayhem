import curses
from contextlib import contextmanager
from typing import Any, Sequence

from ui.palette import Pairs


class Canvas:
    stdscr: curses.window
    offset: int
    win: curses.window
    cursor: int

    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self.offset = 0
        self._build()
        self.win.nodelay(True)
        self.win.timeout(10)

    def _build(self) -> None:
        y_max, x_max = self.stdscr.getmaxyx()
        h, w = y_max - self.offset - 1, x_max - 2
        self.win = curses.newwin(h, w, self.offset, 1)
        self.win.keypad(True)
        self.cursor = 1

    rebuild = _build

    @contextmanager
    def blocking(self):
        self.win.nodelay(False)
        self.win.timeout(-1)
        try:
            yield
        finally:
            self.win.nodelay(True)
            self.win.timeout(10)

    def _draw(self, text: str, pair: int = Pairs.BASE) -> None:
        h, w = self.win.getmaxyx()
        if self.cursor >= h - 1:
            return

        self.win.move(self.cursor, 0)
        self.win.clrtoeol()

        x = max(0, (w - len(text)) // 2)

        self.win.addnstr(self.cursor, x, text, w - x - 1, pair)
        self.cursor += 1

    def draw_lines(
        self, lines: Sequence[str], *, pair: int = Pairs.STATIC, pad: int = 1
    ) -> None:
        base = curses.color_pair(pair)
        for line in lines:
            self._draw(line, base)
        self.cursor += pad

    def draw_header_lines(self, lines: Sequence[str]) -> None:
        self.cursor = 1
        self.draw_lines(lines, pair=Pairs.BASE)
        self.offset = self.cursor

    def draw_menu(
        self,
        lines: Sequence[str],
        *,
        idx: int,
        pair: int = Pairs.BASE,
        pad: int = 1,
    ) -> None:
        base = curses.color_pair(pair)
        hi = base | curses.A_REVERSE
        for i, text in enumerate(lines):
            self._draw(text, hi if i == idx else base)
        self.cursor += pad

    def draw_prompt(self, prompt: str, *, pair: int = Pairs.BASE) -> str:
        _, w = self.win.getmaxyx()
        attr = curses.color_pair(pair)
        x = max(0, (w - (len(prompt) + 1)) // 2)
        self.win.addnstr(self.cursor, x, prompt + " ", w - x - 1, attr)
        self.win.refresh()

        curses.echo()
        self.win.move(self.cursor, x + len(prompt) + 1)
        raw = self.win.getstr(self.cursor, x + len(prompt) + 1, w - x - len(prompt) - 2)
        curses.noecho()

        text = raw.decode("utf-8", errors="ignore")
        self.cursor += 1

        return text

    def erase(self) -> None:
        self.win.move(self.offset, 0)
        self.win.clrtobot()
        self.cursor = self.offset

    def __getattr__(self, name: str) -> Any:
        return getattr(self.win, name)
