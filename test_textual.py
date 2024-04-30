import multiprocessing as mp
from typing import List

import numpy as np
from textual.app import App, ComposeResult
from textual.binding import Binding
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
        width: 3;
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
        margin-right: 2;
        margin-top: 1;
        width: 3;
    }

    """

    def __init__(self, knob: Knob):
        self.knob = knob
        super().__init__(id=f"{knob.name}-mixer")

    def compose(self) -> ComposeResult:
        self.button = Button(self.knob.name, id=self.knob.name)
        yield self.button

        self.progress_bar = ProgressBar(
            total=self.knob.nb_values - 1,
            show_eta=False,
            show_percentage=True,
            id=f"{self.knob.name}-bar",
        )
        self.progress_bar.advance(self.knob.current_index)
        yield self.progress_bar

        self.label = Label(repr(self.knob), id=f"{self.knob.name}-value")
        yield self.label

    def advance(self, step: int):
        previous_index = self.knob.current_index
        self.knob.advance(step)
        if self.knob.current_index == previous_index:
            return
        self.progress_bar.advance(step)  # can advance beyond its total
        self.label.update(repr(self.knob))


class Valmix(App):

    TITLE = "Valmix"

    BINDINGS = [
        Binding(key="down,j", action="next", description="Next"),
        Binding(key="up,k", action="previous", description="Previous"),
        Binding(key="left,h", action="decrease", description="Decrease"),
        Binding(key="right,l", action="increase", description="Increase"),
        Binding(key="q", action="quit", description="Quit"),
    ]

    def __init__(self, knobs: List[Knob]) -> None:
        self.knobs = {knob.name: knob for knob in knobs}
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        for knob in self.knobs.values():
            yield Mixer(knob)
        yield Footer()

    def action_decrease(self) -> None:
        mixer = self.query_one(f"#{self.focused.id}-mixer")
        mixer.advance(-1)

    def action_increase(self) -> None:
        mixer = self.query_one(f"#{self.focused.id}-mixer")
        mixer.advance(+1)

    def action_previous(self) -> None:
        self.screen.focus_previous()

    def action_next(self) -> None:
        self.screen.focus_next()


if __name__ == "__main__":
    foo = Knob("foo", mp.Value("i", 0), range(-10, 10, 3))
    bar = Knob("bar", mp.Value("f", 0.0), np.arange(-1.0, 3.0, 0.1))
    app = Valmix([foo, bar])
    app.run()
