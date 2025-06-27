import curses
import menus
from menus.menu_interface import MenuInterface
from ui.canvas import Canvas
from ui.palette import init_pairs


def main(stdscr: "curses.window") -> None:
    """
    Run the ncurses event loop: initialize menus, route input, and manage menu transitions.
    """

    canvas: Canvas = Canvas(stdscr)
    curses.curs_set(0)
    init_pairs()

    menu_registry: dict[str, type[MenuInterface]] = {
        name: getattr(menus, name) for name in menus.__all__
    }

    next_menu: str | None = "MainMenu"
    current_menu: MenuInterface = menu_registry[next_menu]()

    while next_menu:
        # Instantiate only when transitioning to a new menu
        if not isinstance(current_menu, menu_registry[next_menu]):
            current_menu = menu_registry[next_menu]()

        try:
            # Draw the current menu
            canvas.erase()
            current_menu.draw(canvas)
            curses.doupdate()
            key = canvas.getch()
        except RuntimeError as e:
            # Catch navigation signal
            key = int(str(e))

        # Rebuild canvas on resize
        if key == curses.KEY_RESIZE:
            canvas.clear()
            canvas.refresh()
            canvas.rebuild()
            continue

        # Route to the next menu
        next_menu = current_menu.route(key)


if __name__ == "__main__":
    curses.wrapper(main)
