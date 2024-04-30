import multiprocessing as mp
from typing import List

import numpy as np
from textual.app import App, ComposeResult
from textual.containers import Widget
from textual.widgets import Button, Footer, Header, Label, ProgressBar

from valmix import Knob


class Mixer(Widget):

    DEFAULT_CSS = r"""

    Mixer {
        height: 3;
        layout: horizontal;
    }

    Mixer Button {
        border: wide green;
        margin: 0 2;
        width: 1fr;
    }

    Mixer Button:focus {
        background: $accent;
    }

    Mixer ProgressBar {
        margin-left: 5;
        margin-right: 0;
        margin-top: 1;
        width: 6fr;
    }

    Mixer Bar {
        width: 1fr;
    }

    Mixer Label {
        margin-left: 0;
        margin-right: 5;
        margin-top: 1;
    }

    """

    def __init__(self, knob: Knob):
        self.knob = knob
        super().__init__(id=f"{knob.name}-mixer")

    def compose(self) -> ComposeResult:
        self.button = Button(self.knob.name, id=self.knob.name)
        yield self.button

        self.progress_bar = ProgressBar(
            total=self.knob.nb_values,
            show_eta=False,
            show_percentage=True,
            id=f"{self.knob.name}-bar",
        )
        self.progress_bar.advance(self.knob.current_index)
        yield self.progress_bar

        self.label = Label(repr(self.knob), id=f"{self.knob.name}-value")
        yield self.label

    def advance(self, step: int):
        self.knob.advance(step)
        self.progress_bar.advance(step)
        self.label.update(repr(self.knob))


class Valmix(App):

    TITLE = "Valmix"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, knobs: List[Knob]) -> None:
        self.knobs = {knob.name: knob for knob in knobs}
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        for knob in self.knobs.values():
            yield Mixer(knob.name)
        yield Footer()

    def key_left(self) -> None:
        knob = self.knobs[self.focused.id]
        progress_bar = self.query_one(f"#{knob.name}-bar")
        label = self.query_one(f"#{knob.name}-value")
        progress_bar.advance(-5)
        label.update("kron")

    def key_right(self) -> None:
        bar_id = f"{self.focused.id}-bar"
        self.query_one(f"#{bar_id}").advance(+5)

    def key_up(self) -> None:
        self.screen.focus_previous()

    def key_down(self) -> None:
        self.screen.focus_next()


if __name__ == "__main__":
    foo = Knob("foo", mp.Value("i", 0), range(-10, 10, 3))
    bar = Knob("bar", mp.Value("i", 0), np.arange(-1.0, 3.0, 0.1))
    app = Valmix([foo, bar])
    app.run()
