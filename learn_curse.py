import curses


def main(screen):
    window = curses.newwin(15, 20, 0, 0)
    window.addstr(4, 4, "Hello from 4,4")
    window.refresh()
    curses.napms(2000)

    screen.clear()
    screen.refresh()
    window.mvwin(10, 10)
    window.refresh()
    curses.napms(2000)


# Example usage
if __name__ == "__main__":
    curses.wrapper(main)
