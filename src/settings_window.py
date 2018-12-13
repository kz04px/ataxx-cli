import curses

def show(settings):
    return curses.wrapper(settings_window, settings)

def settings_window(stdscr, settings):
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)

    keys = list(settings.keys())

    quit = False
    y = 0
    k = 0
    while True:
        height, width = stdscr.getmaxyx()

        # Render -- clear
        stdscr.clear()

        # Render -- option title
        stdscr.addstr(0, 0, "- Options -", curses.color_pair(1) | curses.A_BOLD)

        # Render -- option names
        offset = 0
        for key, option in settings.items():
            if offset == y:
                stdscr.addstr(offset+1, 0, key, curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE)
            else:
                stdscr.addstr(offset+1, 0, key, curses.color_pair(1) | curses.A_BOLD)

            xpos = 12
            # Render -- option values
            for n in option.values:
                asd = F"{n}  "
                stdscr.addstr(offset+1, xpos, asd, curses.color_pair(1) | curses.A_BOLD)

                if option.selected() == n:
                    stdscr.addstr(offset+1, xpos, asd, curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addstr(offset+1, xpos, asd, curses.color_pair(2) | curses.A_BOLD)

                xpos += len(asd)

            offset += 1

        # Render -- Done button
        stdscr.addstr(len(settings)+2, 0, "Press enter to continue", curses.color_pair(1) | curses.A_BOLD)

        # Refresh the screen
        stdscr.refresh()

        # Wait for input
        try:
            event = stdscr.getch()
        except KeyboardInterrupt:
            quit = True
            break

        # Quit if esc pressed
        if event == 27:
            quit = True
            break

        # Check inputs
        if event == curses.KEY_UP or event == ord("w"):
            y -= 1
        elif event == curses.KEY_DOWN or event == ord("s"):
            y += 1
        elif event == curses.KEY_LEFT or event == ord("a"):
            settings[keys[y]].left()
        elif event == curses.KEY_RIGHT or event == ord("d"):
            settings[keys[y]].right()
        elif event == ord(" ") or event == ord("\n"):
            break

        # Keep y in range
        if y < 0:
            y = 0
        elif y > len(keys)-1:
            y = len(keys)-1

    # Don't proceed to the game menu if the user quit
    if quit:
        return False

    return True
