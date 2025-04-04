import curses
from api.admin import AdminAPI
from menu.interface import menu_interface, get_input, draw_centered_text


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
        response = api.create_session()
        if not (session_key := response.get("session_key")):
            raise ValueError("Session key not found in response.")

    except Exception as e:
        draw_centered_text(stdscr, "Failed to create session...", offset + 4, 3)
        stdscr.refresh()
        stdscr.getch()
        return

    draw_centered_text(
        stdscr,
        "Share the server address and session key with the players you want to join:",
        offset + 4,
        2,
    )

    draw_centered_text(
        stdscr,
        f"{session_key}",
        offset + 6,
        1,
    )
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(create_game_menu)  # type: ignore
