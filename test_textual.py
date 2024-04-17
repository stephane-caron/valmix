from typing import List

from textual.app import App, ComposeResult
from textual.containers import Widget
from textual.widgets import Button, Footer, Header, ProgressBar


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
        margin: 1 5;
        width: 6fr;
    }

    Mixer Bar {
        width: 1fr;
    }

    """

    def __init__(self, label):
        self.label = label
        super().__init__()

    def compose(self) -> ComposeResult:
        self.button = Button(self.label, id=self.label)
        yield self.button

        self.progress_bar = ProgressBar(
            total=100,
            show_eta=False,
            show_percentage=True,
            id=f"{self.label}-bar",
        )
        self.progress_bar.advance(50)
        yield self.progress_bar


class Valmix(App):

    TITLE = "Valmix"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, values: List[str]) -> None:
        self.values = values
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        for value_name in self.values:
            yield Mixer(value_name)
        yield Footer()

    def key_left(self) -> None:
        bar_id = f"{self.focused.id}-bar"
        self.query_one(f"#{bar_id}").advance(-5)

    def key_right(self) -> None:
        bar_id = f"{self.focused.id}-bar"
        self.query_one(f"#{bar_id}").advance(+5)

    def key_up(self) -> None:
        self.screen.focus_previous()

    def key_down(self) -> None:
        self.screen.focus_next()


if __name__ == "__main__":
    app = Valmix(["foo", "bar"])
    app.run()
