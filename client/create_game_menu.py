import curses
from layout import load_logo, draw_header


def create_game_menu(stdscr):
    curses.curs_set(1)
    logo = load_logo()
    offset = draw_header(stdscr, logo)
    h, w = stdscr.getmaxyx()

    fields = ["Server address", "Admin key"]
    values = ["", ""]
    selected = 0

    while True:
        stdscr.clear()
        draw_header(stdscr, logo)

        for idx, field in enumerate(fields):
            prefix = "> " if idx == selected else "  "
            val = values[idx] if values[idx] else "< >"
            line = f"{prefix}{field}: {val}"
            x = w // 2 - len(line) // 2
            y = offset + 2 + idx
            attr = curses.color_pair(1) if idx == selected else curses.color_pair(2)
            stdscr.attron(attr)
            stdscr.addstr(y, x, line)
            stdscr.attroff(attr)

        btn_label = "[ Create Game ]"
        btn_x = w // 2 - len(btn_label) // 2
        btn_y = offset + 5
        attr = curses.color_pair(1) if selected == 2 else curses.color_pair(2)
        stdscr.attron(attr)
        stdscr.addstr(btn_y, btn_x, btn_label)
        stdscr.attroff(attr)

        stdscr.refresh()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % 3
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % 3
        elif key in (ord("\n"), curses.KEY_ENTER, ord("i")):
            if selected < 2:
                curses.echo()
                prompt_len = len(fields[selected]) + 4
                line_x = w // 2 - (prompt_len + len("[enter text]")) // 2 + prompt_len
                line_y = offset + 2 + selected
                stdscr.move(line_y, line_x)
                stdscr.clrtoeol()
                stdscr.refresh()

                user_input = ""
                while True:
                    ch = stdscr.getch()
                    if ch in (10, 13, 27):
                        break
                    elif ch in (curses.KEY_BACKSPACE, 127, 8):
                        user_input = user_input[:-1]
                        stdscr.addstr(line_y, line_x, " " * (w - line_x - 1))
                        stdscr.move(line_y, line_x)
                        stdscr.addstr(line_y, line_x, user_input)
                        stdscr.move(line_y, line_x + len(user_input))
                    else:
                        user_input += chr(ch)
                        stdscr.addstr(line_y, line_x, user_input)

                curses.noecho()
                values[selected] = user_input
            else:
                stdscr.clear()
                stdscr.addstr(
                    0, 0, f"Creating game at {values[0]} with key {values[1]}"
                )
                stdscr.addstr(2, 0, "Press any key to return.")
                stdscr.refresh()
                stdscr.getch()
                break
        elif key == 27:
            break

    curses.curs_set(0)
