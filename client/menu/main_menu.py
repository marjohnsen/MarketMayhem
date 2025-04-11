import curses
from menu.interface import menu_interface
from menu.host_menu import host_menu

information = []

choices = ["Join Game", "Host Menu", "Exit"]


@menu_interface("menu/ascii_art/marketmayhem.txt", information, choices)
def main_menu(stdscr, options, current_idx, header, offset):  # type: ignore
    if options[current_idx] == options[0]:
        # lobby_menu(stdscr)
        pass
    elif options[current_idx] == options[1]:
        host_menu(stdscr)  # type: ignore
        pass
    elif options[current_idx] == options[2]:
        return -2


if __name__ == "__main__":
    curses.wrapper(main_menu)  # type: ignore
