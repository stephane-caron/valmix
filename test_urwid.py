#!/usr/bin/env python

import multiprocessing as mp
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
    ("focus heading", "white", "dark red"),
    ("focus line", "black", "dark red"),
    ("focus options", "black", "light gray"),
]

focus_map = {
    "heading": "focus heading",
    "options": "focus options",
    "line": "focus line",
}


class SelectableColumns(urwid.Columns):

    def __init__(self) -> None:
        super().__init__([], dividechars=1)

    def open_box(self, box: urwid.Widget) -> None:
        if self.contents:
            del self.contents[self.focus_position + 1 :]
        self.contents.append(
            (
                urwid.AttrMap(box, "options", focus_map),
                self.options(urwid.GIVEN, 24),
            )
        )
        self.focus_position = len(self.contents) - 1


class ValueEditor(urwid.WidgetWrap):

    def __init__(self, values: List[mp.Value]):
        graph = urwid.BarGraph(
            ["bg background", "bg 1", "bg 2"],
            satt={(1, 0): "bg 1 smooth", (2, 0): "bg 2 smooth"},
        )
        graph_wrap = urwid.WidgetWrap(graph)
        self.columns = SelectableColumns()
        self.columns.open_box(graph_wrap)
        self.columns.open_box(graph_wrap)
        window = urwid.LineBox(self.columns)
        window = urwid.AttrMap(window, "contour")

        self.graph = graph
        super().__init__(window)

    def main(self):
        loop = urwid.MainLoop(self, palette, unhandled_input=exit_on_q)
        self.update(loop)
        loop.run()

    def update(self, loop=None, user_data=None):
        max_value = 10
        self.graph.set_data(
            bardata=[[self.columns.focus_position]],
            top=max_value,
            hlines=[80, 30],
        )
        loop.set_alarm_in(0.2, self.update)


if __name__ == "__main__":
    foo = mp.Value("i", 1)
    bar = mp.Value("i", 12)
    editor = ValueEditor(values=[foo, bar])
    editor.main()
