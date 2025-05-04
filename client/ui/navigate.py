import curses
from typing import Optional


class Navigate:
    SELECT = -1
    BACK = -2

    _UP_KEYS = {curses.KEY_UP, ord("k")}
    _DOWN_KEYS = {curses.KEY_DOWN, ord("j")}
    _ENTER = {curses.KEY_ENTER, 10, 13}
    _BACK = {27, curses.KEY_BACKSPACE, 127}

    def __init__(self, pos: int, lower: int, upper: int) -> None:
        if not lower <= pos <= upper:
            raise ValueError("pos must lie between lower and upper")
        self.pos = pos
        self.lower = lower
        self.upper = upper

    def move(self, key: int) -> Optional[int]:
        if key == -1:
            return None

        if key in self._UP_KEYS:
            self.pos = max(self.lower, self.pos - 1)
            return self.pos

        if key in self._DOWN_KEYS:
            self.pos = min(self.upper, self.pos + 1)
            return self.pos

        if key in self._ENTER:
            return self.SELECT

        if key in self._BACK:
            return self.BACK

        return self.pos

    __call__ = move
