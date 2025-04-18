import curses
from api.admin import AdminAPI
from api.singleton import SingletonMeta
from menu.interface import menu_interface
from menu.create_game_menu import create_game_menu


def host_menu(stdscr):
    admin_api = SingletonMeta._instances.get(AdminAPI)
    if admin_api:
        result = connected_menu(stdscr)  # type: ignore
    else:
        result = disconnected_menu(stdscr)  # type: ignore
    if result == -2:
        return -2


@menu_interface("menu/ascii_art/admin_menu.txt", choices=["Create Game", "Go Back"])
def disconnected_menu(stdscr, choices, current_idx, header, offset):
    selection = choices[current_idx]
    if selection == "Create Game":
        create_game_menu(stdscr)  # type: ignore
        return -2
    elif selection == "Go Back":
        stdscr.refresh()
        return -2


@menu_interface(
    "menu/ascii_art/admin_menu.txt",
    choices=["Create Game", "Start Game", "Stop Game", "Go Back"],
)
def connected_menu(stdscr, choices, current_idx, header, offset):
    selection = choices[current_idx]
    if selection == "Create Game":
        create_game_menu(stdscr)  # type: ignore
    elif selection == "Start Game":
        pass
    elif selection == "Stop Game":
        pass
    elif selection == "Go Back":
        return -2


if __name__ == "__main__":
    curses.wrapper(host_menu)
