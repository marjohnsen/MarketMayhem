import curses
from menu.interface import menu_interface, draw_centered_text
from menu.create_game_menu import create_game_menu
from api.singleton import SingletonMeta
from api.admin import AdminAPI


options = ["Create Session", "Active Session", "Go Back"]


@menu_interface("menu/ascii_art/admin_menu.txt", options)
def admin_menu(stdscr, options, current_idx, header, offset):  # type: ignore
    stdscr.move(offset, 0)
    stdscr.clrtobot()

    if options[current_idx] == options[0]:
        create_game_menu(stdscr)  # type: ignore

    elif options[current_idx] == options[1]:
        if AdminAPI in SingletonMeta._instances:
            stdscr.move(offset, 0)
            stdscr.clrtobot()

            server_address = SingletonMeta._instances[AdminAPI].server_address
            session_key = SingletonMeta._instances[AdminAPI].session_key

            draw_centered_text(
                stdscr, f"Server Address: {server_address}", offset + len(options), 2
            )
            draw_centered_text(
                stdscr, f"Session Key: {session_key}", offset + len(options) + 1, 2
            )
            stdscr.refresh()
            stdscr.getch()

    elif options[current_idx] == options[2]:
        return -2


if __name__ == "__main__":
    curses.wrapper(admin_menu)  # type: ignore
