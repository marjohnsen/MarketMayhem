import curses
from api.admin import AdminAPI
from menu.interface import draw_centered_text, get_input, load_header, init_colors


def create_game_menu(stdscr):
    init_colors()
    curses.curs_set(1)
    stdscr.clear()

    header = load_header("menu/ascii_art/create_game.txt")
    offset = len(header) + 2
    center = stdscr.getmaxyx()[1] // 2 - max(len(line) for line in header) // 2

    for i, line in enumerate(header):
        draw_centered_text(stdscr, line, i, 2)

    stdscr.refresh()

    address = get_input(stdscr, "Enter server address: ", offset + 1, center)
    admin_key = get_input(stdscr, "Enter admin key: ", offset + 2, center)
    stdscr.addstr(offset + 2, center + 17, "*" * len(admin_key), curses.color_pair(2))
    epochs = get_input(stdscr, "Enter number of epochs: ", offset + 3, center)
    timestep = get_input(stdscr, "Enter time between each epoch: ", offset + 4, center)

    stdscr.refresh()

    try:
        api = AdminAPI(address, admin_key)
        game_key = api.create_game(epochs, timestep)
        if not game_key:
            raise ValueError("Game key not found.")
    except Exception as e:
        stdscr.clear()
        draw_centered_text(stdscr, f"Error: {str(e)}", offset + 6, center)
        stdscr.refresh()
        stdscr.getch()
        return -2

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
