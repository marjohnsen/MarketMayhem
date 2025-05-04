from menu.interface import menu_interface, draw_centered_text
from api.admin import AdminAPI
from api.singleton import SingletonMeta

options = []


@menu_interface("menu/ascii_art/admin_menu.txt", options)
def game_info_menu(stdscr, options, current_idx, header, offset):  # type: ignore
    if AdminAPI in SingletonMeta._instances:
        stdscr.move(offset, 0)
        stdscr.clrtobot()

        admin_api = SingletonMeta._instances[AdminAPI]
        server_address = admin_api.server_address
        game_key = admin_api.game_key
        epochs = admin_api.epochs
        timestep = admin_api.timestep

        draw_centered_text(
            stdscr, f"Server Address: {server_address}", offset + len(options), 2
        )

        draw_centered_text(
            stdscr, f"Game Key: {game_key}", offset + len(options) + 1, 2
        )

        draw_centered_text(
            stdscr, f"Steps to simulate: {epochs}", offset + len(options) + 3, 2
        )

        draw_centered_text(
            stdscr, f"Time between each step: {timestep}", offset + len(options) + 4, 2
        )

        stdscr.refresh()
        stdscr.getch()
