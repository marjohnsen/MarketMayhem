import curses

from api.admin import AdminAPI
from api.singleton import SingletonMeta
from menu.create_game_menu import create_game_menu
from menu.interface import menu_interface


def host_menu(stdscr):
    while True:
        if api := SingletonMeta._instances.get(AdminAPI):
            info = [
                f"Game Key: {api.game_key}",
                f"Address:  {api.server_address}",
                f"Status:   {api.game_status().get('status')}",
            ]
            result = connected_menu(stdscr, information=info)  # type: ignore
        else:
            result = disconnected_menu(stdscr)  # type: ignore

        if result == -2:
            break


@menu_interface(
    "menu/ascii_art/admin_menu.txt",
    choices=["Create New Game", "Start Game", "Stop Game", "Terminate"],
)
def connected_menu(stdscr, choices, information, current_idx, *_):
    api = SingletonMeta._instances[AdminAPI]
    if choices[current_idx] == "Create New Game":
        AdminAPI.delete()
        create_game_menu(stdscr)
        return 0
    elif choices[current_idx] == "Start Game":
        api.start_game()
        return 0
    elif choices[current_idx] == "Stop Game":
        api.stop_game()
        return 0
    elif choices[current_idx] == "Terminate":
        AdminAPI.delete()
        return -2


@menu_interface(
    "menu/ascii_art/admin_menu.txt",
    choices=["Create Game", "Go Back"],
)
def disconnected_menu(stdscr, choices, information, current_idx, *_):
    if choices[current_idx] == "Create Game":
        AdminAPI.delete()
        create_game_menu(stdscr)
        return 0
    elif choices[current_idx] == "Go Back":
        return -2


if __name__ == "__main__":
    curses.wrapper(host_menu)
