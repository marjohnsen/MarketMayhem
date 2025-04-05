from menu.interface import menu_interface

options = []


@menu_interface("menu/ascii_art/admin_menu.txt", options)
def manage_game_menu(stdscr, options, current_idx, header, offset):  # type: ignore
    if AdminAPI in SingletonMeta._instances:
        stdscr.move(offset, 0)
        stdscr.clrtobot()

        server_address = SingletonMeta._instances[AdminAPI].server_address
        game_key = SingletonMeta._instances[AdminAPI].game_key

        draw_centered_text(
            stdscr, f"Server Address: {server_address}", offset + len(options), 2
        )
        draw_centered_text(
            stdscr, f"Game Key: {game_key}", offset + len(options) + 1, 2
        )
        stdscr.refresh()
        stdscr.getch()
