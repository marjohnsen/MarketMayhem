import curses


class Canvas:
    def __init__(self, stdscr, h=None, w=None, y=0, x=0):
        max_y, max_x = stdscr.getmaxyx()
        self.h = h or max_y - 2
        self.w = w or max_x - 2
        self.y, self.x = y + 1, x + 1
        self.win = curses.newwin(self.h, self.w, self.y, self.x)
        self.win.keypad(True)

    def getch(self):
        return self.win.getch()

    def clear(self):
        self.win.erase()

    def addstr(self, y, x, text, attr=0):
        self.win.addstr(y, x, text, attr)

    def flush(self):
        self.win.noutrefresh()
