import curses
from menu.interface import menu_interface
from menu.host_menu import host_menu

information = []
choices = ["Join Game", "Host Menu", "Exit"]


@menu_interface("menu/ascii_art/marketmayhem.txt", information, choices)
def main_menu(stdscr, choices, current_idx, header, offset):
    selection = choices[current_idx]
    if selection == "Join Game":
        pass
    elif selection == "Host Menu":
        host_menu(stdscr)
    elif selection == "Exit":
        return -2


if __name__ == "__main__":
    curses.wrapper(main_menu)  # type: ignore
