import curses
from menu.interface import menu_interface
from menu.manage_game_menu import manage_game_menu
from menu.create_game_menu import create_game_menu
from api.singleton import SingletonMeta
from api.admin import AdminAPI


options = ["Create Game", "Go Back"]


@menu_interface("menu/ascii_art/admin_menu.txt", options)
def admin_menu(stdscr, options, current_idx, header, offset):  # type: ignore
    stdscr.move(offset, 0)
    stdscr.clrtobot()

    if options[current_idx] == "Create Game":
        create_game_menu(stdscr)  # type: ignore

    if AdminAPI in SingletonMeta._instances and len(options) > 2:
        if options[current_idx] == "Manage Game":
            manage_game_menu(stdscr)  # type: ignore

    elif options[current_idx] == "Go Back":
        return -2

    if AdminAPI in SingletonMeta._instances:
        options.append(options[1])
        options[1] = "Manage Game"


if __name__ == "__main__":
    curses.wrapper(admin_menu)  # type: ignore
