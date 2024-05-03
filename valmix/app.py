from typing import List

import textual.app
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header

from .knob import Knob
from .mixer import Mixer


class App(textual.app.App):

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
