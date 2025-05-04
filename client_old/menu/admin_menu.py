import curses

from api.admin import AdminAPI
from api.singleton import SingletonMeta
from menu.interface import menu_interface



options = ["Create Game", "Go Back"]

@menu_interface("menu/ascii_art/admin_menu.txt", options)
def admin_menu(stdscr, options, current_idx, header, offset):  # type: ignore

# options = ["Create Game", "Go Back"]

# @menu_interface("menu/ascii_art/admin_menu.txt", options)
# def host_menu(stdscr, options, current_idx, header, offset):  # type: ignore
#     admin_api = SingletonMeta._instances.get(AdminAPI)
#
#     stdscr.move(offset, 0)
#     stdscr.clrtobot()
#
#     if (options[current_idx] == "Create Game") and not admin_api:
#         # create_game_menu(stdscr)  # type: ignore
#         admin_api = True
#
#     if (options[current_idx] == "New Game") and admin_api:
#         del SingletonMeta._instances[AdminAPI]
#
#     if (options[current_idx] == "Start Game") and admin_api:
#         if options[current_idx] == "Start Game":
#             #admin_api.start_game()
#
#     if (options[current_idx] == "Stop Game") and admin_api:
#         if options[current_idx] == "Stop Game":
#             admin_api.stop_game()
#
#     if (options[current_idx] == "Game Info") and admin_api:
#         if options[current_idx] == "Game Info":
#             game_info_menu(stdscr)  # type: ignore
#
#     elif options[current_idx] == "Go Back":
#         return -2
#
#     if ("Manage Game" not in options) and (admin_api):
#         options.append(options[1])
#         options[1] = "Manage Game"
#
#
# if __name__ == "__main__":
#     curses.wrapper(admin_menu)  # type: ignore
