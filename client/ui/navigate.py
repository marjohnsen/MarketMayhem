import curses
from typing import Optional


class Navigation:
    SELECT: int = -1
    BACK: int = -2

    _UP: set[int] = {curses.KEY_UP, ord("k")}
    _DOWN: set[int] = {curses.KEY_DOWN, ord("j")}
    _ENTER: set[int] = {curses.KEY_ENTER, 10, 13}
    _BACK: set[int] = {27, curses.KEY_BACKSPACE, 127, ord("q")}

    size: int
    pos: int
    wrap: bool

    def __init__(self, size: int, pos: int = 0, wrap: bool = True) -> None:
        assert size > 0, "size must be positive"
        self.size = size
        self.pos = pos % size
        self.wrap = wrap

    def __call__(self, key: int) -> Optional[int]:
        if key == -1:
            return None
        if key in self._UP:
            new_pos: int = (
                (self.pos - 1) % self.size if self.wrap else max(0, self.pos - 1)
            )
            self.pos = new_pos
            return self.pos
        if key in self._DOWN:
            new_pos: int = (
                (self.pos + 1) % self.size
                if self.wrap
                else min(self.size - 1, self.pos + 1)
            )
            self.pos = new_pos
            return self.pos
        if key in self._ENTER:
            return self.SELECT
        if key in self._BACK:
            return self.BACK
        return self.pos
