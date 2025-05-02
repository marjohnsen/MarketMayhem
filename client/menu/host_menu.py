import curses

from api.admin import AdminAPI
from api.singleton import SingletonMeta
from menu.create_game_menu import create_game_menu
from menu.interface import menu_interface


def host_menu(stdscr):
    while True:
        if api := SingletonMeta._instances.get(AdminAPI):
            result = connected_menu(  # type: ignore
                stdscr,
                information=lambda: [
                    f"  Status: {api.game_status().get('status')}",
                    " ",
                    f"Game Key: {api.game_key}",
                    f" Address: {api.server_address}",
                    " ",
                    f" Players:",
                ]
                + [
                    f"{' ' * 9}-{name}"
                    for name in api.list_players().get("players", [])
                ],
            )
        else:
            result = disconnected_menu(stdscr)  # type: ignore
            if result == 1:
                continue
        if result == -2:
            break


@menu_interface(
    "menu/ascii_art/admin_menu.txt",
    choices=[
        "Create New Game",
        "Update Status",
        "Start Game",
        "End Game",
        "Abort",
    ],
    refresh_ms=1000,
)
def connected_menu(stdscr, choices, information, current_idx, *_):
    api = SingletonMeta._instances[AdminAPI]
    if choices[current_idx] == "Create New Game":
        AdminAPI.delete()
        create_game_menu(stdscr)
        return 0
    if choices[current_idx] == "Update Status":
        return 1
    if choices[current_idx] == "Start Game":
        try:
            api.start_game()
        except Exception as e:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Error: {str(e)}")
            stdscr.refresh()
            stdscr.getch()
            return 1
        return 0
    if choices[current_idx] == "End Game":
        try:
            api.stop_game()
        except Exception as e:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Error: {str(e)}")
            stdscr.refresh()
            stdscr.getch()
            return 1
        return 0
    if choices[current_idx] == "Abort":
        AdminAPI.delete()
        return 1


@menu_interface(
    "menu/ascii_art/admin_menu.txt",
    choices=["Create Game", "Go Back"],
)
def disconnected_menu(stdscr, choices, information, current_idx, *_):
    if choices[current_idx] == "Create Game":
        AdminAPI.delete()
        create_game_menu(stdscr)
        return 1
    if choices[current_idx] == "Go Back":
        return -2


if __name__ == "__main__":
    curses.wrapper(host_menu)
