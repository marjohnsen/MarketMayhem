import curses
from pathlib import Path
from typing import List


class Header:
    def __init__(self, path: str | Path) -> None:
        raw: List[str] = (
            Path(path).expanduser().read_text(encoding="utf‑8").splitlines()
        )
        self.lines: List[str] = [ln.rstrip("\n") for ln in raw] or [""]

    @staticmethod
    def _centre(win: curses.window, text_width: int) -> int:
        _, w = win.getmaxyx()
        return max(0, (w - text_width) // 2)

    def draw(self, win: curses.window, y: int, pair: int) -> int:
        for i, line in enumerate(self.lines):
            x = self._centre(win, len(line))
            win.attron(curses.color_pair(pair))
            win.addnstr(y + i, x, line, win.getmaxyx()[1] - x - 1)
            win.attroff(curses.color_pair(pair))
        return len(self.lines) + 1
