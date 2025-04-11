import curses

from api.admin import AdminAPI
from api.singleton import SingletonMeta
from menu.interface import menu_interface

# NEED TO REFRESH SOMEWHERE!


def host_menu(stdscr):
    while True:
        admin_api = SingletonMeta._instances.get(AdminAPI)

        if admin_api:
            result = connected_host_menu(stdscr)  # type: ignore
        else:
            result = disconnected_host_menu(stdscr)  # type: ignore

        if result == -2:
            break


@menu_interface("menu/ascii_art/admin_menu.txt", choices=["Create Game", "Go Back"])
def disconnected_host_menu(stdscr, choices, current_idx, header, offset):
    selection = choices[current_idx]

    if selection == "Create Game":
        SingletonMeta._instances[AdminAPI] = AdminAPI("localhost:5000", "123")
        return -1
    elif selection == "Go Back":
        return -2


@menu_interface(
    "menu/ascii_art/admin_menu.txt",
    choices=["Create Game", "Start Game", "Stop Game", "Go Back"],
)
def connected_host_menu(stdscr, choices, current_idx, header, offset):
    selection = choices[current_idx]

    if selection == "Create Game":
        pass
    elif selection == "Start Game":
        pass
    elif selection == "Stop Game":
        pass
    elif selection == "Go Back":
        return -2


if __name__ == "__main__":
    curses.wrapper(host_menu)

if __name__ == "__main__":
    curses.wrapper(host_menu)  # type: ignore
