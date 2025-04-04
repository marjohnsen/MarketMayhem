import curses
from menu.interface import menu_interface

# from menu.lobby_menu import lobby_menu
from menu.admin_menu import admin_menu

options = ["Join Lobby", "Admin Menu", "Exit"]


@menu_interface("menu/ascii_art/marketmayhem.txt", options)
def main_menu(stdscr, options, current_idx, header, offset):  # type: ignore
    stdscr.move(offset, 0)
    stdscr.clrtobot()
    if options[current_idx] == options[0]:
        # lobby_menu(stdscr)
        pass
    elif options[current_idx] == options[1]:
        admin_menu(stdscr)  # type: ignore
    elif options[current_idx] == options[2]:
        return -2


if __name__ == "__main__":
    curses.wrapper(main_menu)  # type: ignore
