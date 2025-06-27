from pathlib import Path
from typing import Any, Optional

from ui.canvas import Canvas
from ui.navigate import Navigation

from menus.menu_interface import MenuInterface


class MainMenu(MenuInterface):
    nav: Navigation
    options: list[str]
    header_lines: list[str]

    def __init__(self) -> None:
        self.options = ["Join Game", "Host Menu", "Exit"]
        self.nav = Navigation(len(self.options))
        self.header_lines = (
            Path("ui/ascii_art/marketmayhem.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        )

    def draw(self, canvas: Canvas) -> None:
        canvas.erase()
        canvas.draw_header_lines(self.header_lines)
        canvas.draw_menu(self.options, idx=self.nav.pos)
        canvas.noutrefresh()

    def route(self, key: int) -> Optional[Any]:
        if self.nav(key) == Navigation.SELECT:
            if self.nav.pos == 0:
                return None  # TODO: implement Join Game
            elif self.nav.pos == 1:
                return "HostMenu"
            elif self.nav.pos == 2:
                return None
        else:
            return "MainMenu"
