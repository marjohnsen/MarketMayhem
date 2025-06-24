import curses
from ui.navigate import Navigation
from ui.canvas import Canvas
from ui.header import Header
from ui.palette import init_pairs, Pairs


def main(stdscr):
    # Initalize
    curses.curs_set(0)
    init_pairs()

    header = Header.from_file("ui/ascii_art/marketmayhem.txt")
    canvas = Canvas(stdscr, len(header.lines) + 1)

    choices = ["Join Game", "Host Menu", "Exit"]
    navigate = Navigation(len(choices))

    stdscr.nodelay(True)
    stdscr.timeout(100)

    canvas.nodelay(True)
    canvas.timeout(100)

    while True:
        # Navigation
        key = canvas.getch()
        action = navigate(key)

        # Rebuild on resize
        if key == curses.KEY_RESIZE:
            canvas.rebuild()
            continue

        # Clear previous frame
        stdscr.erase()
        canvas.erase()

        # Stage the header
        header.draw(stdscr, 1, Pairs.STANDARD)
        stdscr.noutrefresh()

        # Stage the canvas
        canvas.draw_list(choices, selected=navigate.pos, pair=Pairs.STANDARD)
        canvas.noutrefresh()

        # Make decisions based on navigation
        if action == Navigation.SELECT:
            match choices[navigate.pos]:
                case "Exit":
                    break
                case "Join Game":
                    break
                case "Host Menu":
                    break
        elif action == Navigation.BACK:
            break

        # Push frame to the terminal
        curses.doupdate()


if __name__ == "__main__":
    curses.wrapper(main)
