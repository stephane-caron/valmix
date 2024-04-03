#!/usr/bin/env python

from typing import List
import urwid


def exit_on_q(key: str) -> None:
    if key.lower() == "q":
        raise urwid.ExitMainLoop()


palette: List[List[str]] = [
    ("contour", "black", "light gray", "standout"),
    ("bg background", "light gray", "black"),
    ("bg 1", "black", "dark blue", "standout"),
    ("bg 2", "black", "dark cyan", "standout"),
    ("bg 1 smooth", "dark blue", "black"),
    ("bg 2 smooth", "dark cyan", "black"),
]


class ValueEditor(urwid.WidgetWrap):

    def __init__(self):
        graph = urwid.BarGraph(
            ["bg background", "bg 1", "bg 2"],
            satt={(1, 0): "bg 1 smooth", (2, 0): "bg 2 smooth"},
        )
        graph_wrap = urwid.WidgetWrap(graph)
        empty_line = urwid.AttrMap(urwid.SolidFill(" "), "contour")
        window = urwid.Columns(
            [
                (urwid.WEIGHT, 2, empty_line),
                (2, graph_wrap),
                (urwid.WEIGHT, 2, empty_line),
                (urwid.WEIGHT, 2, empty_line),
                (2, graph_wrap),
                (urwid.WEIGHT, 2, empty_line),
            ],
        )
        window = urwid.LineBox(window)
        window = urwid.AttrMap(window, "contour")

        self.graph = graph
        self.i = 0
        super().__init__(window)

    def main(self):
        loop = urwid.MainLoop(self, palette, unhandled_input=exit_on_q)
        self.update(loop)
        loop.run()

    def update(self, loop=None, user_data=None):
        max_value = 100
        self.i = (self.i + 0.1) % max_value
        self.graph.set_data(
            bardata=[[self.i + 0.5]],
            top=max_value,
            hlines=[80, 30],
        )
        loop.set_alarm_in(0.2, self.update)


if __name__ == "__main__":
    editor = ValueEditor()
    editor.main()
