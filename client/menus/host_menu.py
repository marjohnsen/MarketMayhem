from pathlib import Path
from typing import Any, Optional

from menus.menu import Menu

from ui.canvas import Canvas
from ui.navigate import Navigation

from api.admin import AdminAPI


class HostMenu(Menu):
    options: list[str]
    nav: Navigation
    header_lines: list[str]

    def __init__(self) -> None:
        self.connected = False

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

        else:
            self.options = [
                "Create New Game",
                "Exit",
            ]

            canvas.draw_menu(self.options, idx=self.nav.pos)

            self.connected = True

        canvas.noutrefresh()

    def route(self, key: int) -> Optional[Any]:
        action = self.nav(key)

        if self.connected:
            None  # TODO: implement routing the connected options
        else:
            None  # TODO: implement routing the disconnected options
