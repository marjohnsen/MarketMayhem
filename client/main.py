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

    canvas = Canvas(stdscr)
    header = Header("ui/ascii_art/marketmayhem.txt")

    while True:
        stdscr.erase()
        # stdscr.border()
        header.draw(stdscr, y=0, pair=Pairs.STANDARD)

        canvas.win.border()

        canvas.flush()
        stdscr.noutrefresh()
        curses.doupdate()


if __name__ == "__main__":
    curses.wrapper(main)
