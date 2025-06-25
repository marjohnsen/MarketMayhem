import curses
from enum import IntEnum, auto


class Pairs(IntEnum):
    BASE = auto()
    SELECTED = auto()
    STATIC = auto()
    WARNING = auto()


def init_pairs():
    if not curses.has_colors():
        return

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(Pairs.BASE, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(Pairs.SELECTED, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(Pairs.STATIC, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(Pairs.WARNING, curses.COLOR_BLACK, curses.COLOR_RED)
