import curses
from create_game_menu import create_game_menu
from layout import load_logo, draw_header, draw_menu_list, get_input

menu = ["Join Game", "Create Game", "Exit"]


def draw_main(stdscr, selected_idx):
    stdscr.clear()
    logo = load_logo()
    offset = draw_header(stdscr, logo)
    draw_menu_list(stdscr, menu, selected_idx, offset)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    selected_idx = 0
    while True:
        draw_main(stdscr, selected_idx)
        key = stdscr.getch()
        if key in (curses.KEY_UP, ord("k")) and selected_idx > 0:
            selected_idx -= 1
        elif key in (curses.KEY_DOWN, ord("j")) and selected_idx < len(menu) - 1:
            selected_idx += 1
        elif key in (curses.KEY_ENTER, ord("\n")):
            selected = menu[selected_idx]
            if selected == "Exit":
                break
            elif selected == "Create Game":
                create_game_menu(stdscr)
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, f"You selected '{selected}'. Press any key.")
                stdscr.getch()
        elif key == 27:
            break


if __name__ == "__main__":
    curses.wrapper(main)
