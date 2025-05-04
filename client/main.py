import curses
from ui.canvas import Canvas
from ui.navigate import Navigate
from ui.palette import init_pairs, Pairs
from ui.header import Header


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    init_pairs()

    canvas = Canvas(stdscr, h=10, w=40, y=1, x=1)
    header = Header("ui/ascii_art/marketmayhem.txt")

    while True:
        stdscr.erase()

        stdscr.border()
        header.draw(stdscr, y=0, pair=Pairs.STANDARD)
        stdscr.noutrefresh()

        canvas.clear()
        canvas.win.border()

        canvas.flush()
        curses.doupdate()


if __name__ == "__main__":
    curses.wrapper(main)
