import curses


def wintest(screen):
    window = curses.newwin(15, 20, 0, 0)
    window.addstr(4, 4, "Hello from 4,4")
    window.refresh()
    curses.napms(500)

    screen.clear()
    screen.refresh()
    window.mvwin(10, 10)
    window.refresh()
    curses.napms(500)
    window.mvwin(4, 4)
    screen.refresh()
    window.refresh()
    curses.napms(500)


def main(screen: curses.window):
    screen.clear()
    curses.curs_set(0)

    screen.refresh()
    screen.move(0, 1)
    screen.addstr("1", curses.A_BOLD)
    screen.addstr(":Help  ", 0)
    screen.refresh()

    max_y, max_x = screen.getmaxyx()
    screen.hline(1, 0, curses.ACS_HLINE, max_x)
    screen.refresh()

    curses.napms(2000)


# Example usage
if __name__ == "__main__":
    curses.wrapper(main)
