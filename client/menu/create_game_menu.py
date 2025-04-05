import curses

from api.admin import AdminAPI
from api.singleton import SingletonMeta
from menu.interface import draw_centered_text, get_input, menu_interface


@menu_interface("menu/ascii_art/create_game.txt")
def create_game_menu(stdscr, options, current_idx, header, offset):  # type: ignore
    w_term = stdscr.getmaxyx()[1]
    w_header = max(len(line) for line in header)
    center = (w_term // 2) - (w_header // 2)
    address = get_input(stdscr, "Enter server address: ", offset + 1, center)
    key = get_input(stdscr, "Enter admin key: ", offset + 2, center)
    stdscr.addstr(
        offset + 2,
        center + len("Enter admin key: "),
        "*" * len(key),
        curses.color_pair(2),
    )
    stdscr.refresh()

    try:
        api = AdminAPI(address, key)
        response = api.create_game()
        if not (game_key := response.get("game_key")):
            del SingletonMeta._instances[AdminAPI]
            raise ValueError("Game key not found in response.")

    except Exception as e:
        draw_centered_text(stdscr, "Failed to create game...", offset + 4, 3)
        stdscr.refresh()
        stdscr.getch()
        return

    draw_centered_text(
        stdscr,
        "Share the server address and game key with the players you want to join:",
        offset + 4,
        2,
    )

    draw_centered_text(
        stdscr,
        f"{game_key}",
        offset + 6,
        1,
    )
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(create_game_menu)  # type: ignore
