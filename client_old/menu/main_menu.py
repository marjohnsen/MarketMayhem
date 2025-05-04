import curses
from menu.interface import menu_interface
from menu.host_menu import host_menu

choices = ["Join Game", "Host Menu", "Exit"]


@menu_interface("menu/ascii_art/marketmayhem.txt", choices)
def main_menu(stdscr, choices, information, current_idx, header):
    selection = choices[current_idx]
    if selection == "Join Game":
        pass
    elif selection == "Host Menu":
        host_menu(stdscr)
    elif selection == "Exit":
        return -2


if __name__ == "__main__":
    curses.wrapper(main_menu)
