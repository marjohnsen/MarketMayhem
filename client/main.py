import curses
from typing import Optional

from menus.main_menu import MainMenu
from menus.menu import Menu
from ui.canvas import Canvas
from ui.palette import init_pairs


def main(stdscr: curses.window) -> None:
    curses.curs_set(0)
    init_pairs()

    canvas: Canvas = Canvas(stdscr)
    menu: Optional[Menu] = MainMenu()

    while menu is not None:
        key: int = canvas.getch()
        if key == curses.KEY_RESIZE:
            canvas.rebuild()
            continue

        canvas.erase()
        menu.draw(canvas)
        curses.doupdate()
        menu = menu.route(key)


if __name__ == "__main__":
    curses.wrapper(main)
