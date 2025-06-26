from pathlib import Path
from typing import Any, Optional

from ui.canvas import Canvas
from ui.navigate import Navigation

from menus.menu_interface import MenuInterface


class HostMenu(MenuInterface):
    connected: bool
    options: list[str]
    nav: Navigation
    header_lines: list[str]

    def __init__(self) -> None:
        self.connected = False
        self.options = ["Create New Game", "Exit"]
        self.nav = Navigation(len(self.options))
        self.header_lines = (
            Path("ui/ascii_art/marketmayhem.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        )

    def draw(self, canvas: Canvas) -> None:
        canvas.erase()
        canvas.draw_header_lines(self.header_lines)

        if self.connected:
            self.options = [
                "Update Status",
                "Start Game",
                "End Game",
                "Abort",
                "Exit",
            ]
            self.nav = Navigation(len(self.options))

        canvas.draw_menu(self.options, idx=self.nav.pos)

        canvas.noutrefresh()

    def route(self, key: int) -> Optional[Any]:
        if (action := self.nav(key)) == Navigation.SELECT:
            if self.connected:
                if self.nav.pos == 0:
                    return None  # TODO: Update status
                elif self.nav.pos == 1:
                    return None  # TODO: Start game
                elif self.nav.pos == 2:
                    return None  # TODO: End game
                elif self.nav.pos == 3:
                    return None  # TODO: Abort
                elif self.nav.pos == 4:
                    return None  # TODO: Exit to main menu
            else:
                if self.nav.pos == 0:
                    return "CreateGameMenu"
                elif self.nav.pos == 1:
                    return None  # TODO: Exit to main menu
        return self
