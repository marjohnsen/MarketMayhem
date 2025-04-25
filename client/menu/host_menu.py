import curses
from api.admin import AdminAPI
from api.singleton import SingletonMeta
from menu.interface import menu_interface
from menu.create_game_menu import create_game_menu


def host_menu(stdscr):
    admin_api = SingletonMeta._instances.get(AdminAPI)
    if admin_api:
        connected_menu(stdscr, information=[])  # type: ignore
    else:
        disconnected_menu(stdscr)  # type: ignore


@menu_interface(
    "menu/ascii_art/admin_menu.txt",
    choices=["Create New Game", "Start Game", "Stop Game", "Terminate"],
)
def connected_menu(stdscr, choices, information, current_idx, *_):
    if choices[current_idx] == "Create New Game":
        AdminAPI.delete()
        create_game_menu(stdscr)
        connected_menu(stdscr, information=[])  # type: ignore
    elif choices[current_idx] == "Start Game":
        AdminAPI().start_game()
    elif choices[current_idx] == "Stop Game":
        AdminAPI().stop_game()
    elif choices[current_idx] == "Terminate":
        AdminAPI.delete()
        return -2


@menu_interface(
    "menu/ascii_art/admin_menu.txt",
    choices=["Create Game", "Go Back"],
)
def disconnected_menu(stdscr, choices, information, current_idx, *_):
    if choices[current_idx] == "Create Game":
        create_game_menu(stdscr)
        info = [
            f"Game Key: {AdminAPI().game_key}",
            f"Address:  {AdminAPI().server_address}",
            f"Status:   {AdminAPI().game_status().get('status')}",
        ]
        connected_menu(stdscr, information=info)  # type: ignore
    elif choices[current_idx] == "Go Back":
        return -2


if __name__ == "__main__":
    curses.wrapper(host_menu)
