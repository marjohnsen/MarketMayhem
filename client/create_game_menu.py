import curses
import requests
from layout import load_logo, draw_header


def create_game_menu(stdscr):
    curses.curs_set(0)
    logo = load_logo()
    offset = draw_header(stdscr, logo)
    h, w = stdscr.getmaxyx()

    fields = ["Server address", "Admin key"]
    values = ["", ""]
    selected = 0

    def draw_fields(editing=False):
        stdscr.clear()
        draw_header(stdscr, logo)
        for idx, field in enumerate(fields):
            prefix = "> " if idx == selected else "  "
            val = f"[{values[idx]}]" if editing and idx == selected else values[idx]
            line = f"{prefix}{field}: {val}"
            x = w // 2 - len(line) // 2
            y = offset + 2 + idx
            attr = curses.color_pair(1 if idx == selected else 2)
            stdscr.attron(attr)
            stdscr.addstr(y, x, line)
            stdscr.attroff(attr)

        btn_label = "[ Create Game ]"
        btn_x = w // 2 - len(btn_label) // 2
        btn_y = offset + 5
        attr = curses.color_pair(1 if selected == 2 else 2)
        stdscr.attron(attr)
        stdscr.addstr(btn_y, btn_x, btn_label)
        stdscr.attroff(attr)
        stdscr.refresh()

    while True:
        draw_fields()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % 3
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % 3
        elif key in (ord("\n"), curses.KEY_ENTER, ord("i")):
            if selected < 2:
                curses.curs_set(1)
                curses.echo()
                line_prefix = f"> {fields[selected]}: ["
                input_x = w // 2 - len(line_prefix + "]") // 2 + len(line_prefix)
                input_y = offset + 2 + selected
                stdscr.move(input_y, input_x - 1)
                stdscr.addstr("[]")
                stdscr.move(input_y, input_x)

                user_input = values[selected]
                while True:
                    stdscr.addstr(input_y, input_x - 1, f"[{user_input}] ")
                    stdscr.move(input_y, input_x + len(user_input))
                    ch = stdscr.getch()
                    if ch in (10, 13, 27):  # Enter or ESC saves
                        break
                    elif ch in (curses.KEY_BACKSPACE, 127, 8):
                        user_input = user_input[:-1]
                    elif 32 <= ch <= 126:
                        user_input += chr(ch)

                values[selected] = user_input.strip()
                curses.noecho()
                curses.curs_set(0)
            else:
                api_url = f"http://{values[0]}:5000/create_session"
                try:
                    response = requests.post(
                        api_url,
                        json={"admin_key": values[1]},
                        timeout=5,
                    )
                    response.raise_for_status()
                    data = response.json()
                    session_key = data.get("session_key")
                    message = data.get("message")
                except requests.RequestException as e:
                    session_key = None
                    message = f"Error: {e}"

                # Cool centered output with box-drawing chars
                stdscr.clear()

                message_lines = message.split("\n")
                box_width = max(len(session_key or ""), 20) + 4
                box_height = 3
                total_height = len(message_lines) + box_height + 2

                start_y = h // 2 - total_height // 2
                for i, line in enumerate(message_lines):
                    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
                    stdscr.addstr(start_y + i, w // 2 - len(line) // 2, line)
                    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

                if session_key:
                    box_top = start_y + len(message_lines) + 1
                    box_left = w // 2 - box_width // 2
                    stdscr.attron(curses.color_pair(2))

                    # Draw box with box-drawing chars
                    stdscr.addstr(box_top, box_left, "┌" + "─" * (box_width - 2) + "┐")
                    stdscr.addstr(
                        box_top + 1,
                        box_left,
                        "│" + session_key.center(box_width - 2) + "│",
                    )
                    stdscr.addstr(
                        box_top + 2, box_left, "└" + "─" * (box_width - 2) + "┘"
                    )

                    stdscr.attroff(curses.color_pair(2))

                exit_text = "Press any key to continue..."
                stdscr.addstr(
                    box_top + box_height + 1, w // 2 - len(exit_text) // 2, exit_text
                )
                stdscr.refresh()
                stdscr.getch()
                break
        elif key == 27:
            break
