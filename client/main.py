import curses
import menus as menus_pkg
from menus.menu_interface import MenuInterface
from ui.canvas import Canvas
from ui.palette import init_pairs


def main(stdscr):
    menus = {name: getattr(menus_pkg, name) for name in menus_pkg.__all__}
    curses.curs_set(0)
    init_pairs()
    canvas = Canvas(stdscr)
    menu = menus["MainMenu"]()
    while menu:
        canvas.erase()
        menu.draw(canvas)
        curses.doupdate()
        key = canvas.getch()
        if key == curses.KEY_RESIZE:
            canvas.rebuild()
            continue
        if key == -1:
            continue
        nxt = menu.route(key)
        if nxt is None:
            break
        if isinstance(nxt, str):
            menu = menus[nxt]()
        elif isinstance(nxt, type):
            menu = nxt()
        else:
            menu = nxt


if __name__ == "__main__":
    curses.wrapper(main)
