import curses
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from ui.palette import Pairs


@dataclass(slots=True)
class Header:
    lines: Sequence[str]

    @classmethod
    def from_file(cls, path: str | Path) -> "Header":
        text = Path(path).expanduser().read_text(encoding="utf-8").splitlines() or [""]
        return cls(text)

    def draw(self, win: curses.window, y: int = 1, pair: Pairs = Pairs.BASE) -> int:
        _, width = win.getmaxyx()
        attr = curses.color_pair(pair)
        for i, line in enumerate(self.lines):
            x = max(0, (width - len(line)) // 2)
            win.addnstr(y + i, x, line, width - x - 1, attr)
        return len(self.lines) + 1
