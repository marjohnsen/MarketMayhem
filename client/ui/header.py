from pathlib import Path
from dataclasses import dataclass
import curses


@dataclass(slots=True)
class Header:
    lines: list[str]

    @classmethod
    def from_file(cls, path):
        txt = Path(path).expanduser().read_text(encoding="utf-8").splitlines()
        return cls(txt or [""])

    def draw(self, win, y, pair):
        _, w = win.getmaxyx()
        attr = curses.color_pair(pair)
        for i, ln in enumerate(self.lines):
            x = max(0, (w - len(ln)) // 2)
            win.addnstr(y + i, x, ln, w - x - 1, attr)
        return len(self.lines) + 1
