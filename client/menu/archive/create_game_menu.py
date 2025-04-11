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
    epochs = get_input(stdscr, "Enter how many steps to simulate: ", offset + 3, center)
    timestep = get_input(
        stdscr, "Enter the time in seconds between each step: ", offset + 4, center
    )
    stdscr.refresh()

    try:
        api = AdminAPI(address, key)
        response = api.create_game(epochs, timestep)
        if not (game_key := response.get("game_key")):
            del SingletonMeta._instances[AdminAPI]
            raise ValueError("Game key not found in response.")

    except Exception as e:
        draw_centered_text(stdscr, f"{e}", offset + 6, 3)
        stdscr.refresh()
        stdscr.getch()
        return

    draw_centered_text(
        stdscr,
        "Share the server address and game key with the players you want to join:",
        offset + 6,
        2,
    )

    draw_centered_text(
        stdscr,
        f"{game_key}",
        offset + 7,
        1,
    )

    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(create_game_menu)  # type: ignore
