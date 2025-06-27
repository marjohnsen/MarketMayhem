from pathlib import Path
from typing import Any, Optional

from api.admin import AdminAPI
from ui.canvas import Canvas
from ui.navigate import Navigation
from ui.palette import Pairs

from menus.menu_interface import MenuInterface


class CreateGameMenu(MenuInterface):
    nav: Navigation
    header_lines: list[str]

    def __init__(self) -> None:
        self.nav = Navigation(1)
        self.header_lines = (
            Path("ui/ascii_art/create_game.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        )

    def draw(self, canvas: Canvas) -> Any:
        canvas.erase()
        canvas.draw_header_lines(self.header_lines)

        # with canvas.blocking():
        address = canvas.draw_prompt("Enter server address: ")
        admin_key = canvas.draw_prompt("Enter admin key: ")
        epochs = canvas.draw_prompt("Enter number of epochs: ")
        timestep = canvas.draw_prompt("Enter time between each epoch: ")
        game_key = 123

        try:
            api = AdminAPI(address, admin_key)
            response = api.create_game(int(epochs), int(timestep))
            game_key = response.get("game_key")

        except Exception as e:
            canvas.clear()
            AdminAPI.delete()
            canvas.draw_lines([f"Error: {str(e)}"], pair=Pairs.WARNING)
            #        with canvas.blocking():
            canvas.getch()
            raise RuntimeError(f"{Navigation.BACK}")

        canvas.erase()

        canvas.draw_lines(
            [
                "Share the following information with the players you want to join:",
                "",
                f"Server Address: {address}",
                f"Game Key: {game_key}",
            ],
            pair=Pairs.STATIC,
        )

        # with canvas.blocking():
        canvas.getch()

        canvas.noutrefresh()

    def route(self, key: int) -> Optional[Any]:
        return "HostMenu"
