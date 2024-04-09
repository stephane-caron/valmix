from typing import List

from textual.app import App, ComposeResult
from textual.containers import Widget
from textual.widgets import Button, Footer, Header, ProgressBar


class ButtonBar(Widget):

    DEFAULT_CSS = r"""

    ButtonBar {
        height: 3;
        layout: horizontal;
    }

    ButtonBar Button {
        border: wide green;
        margin: 0 2;
        width: 1fr;
    }

    ButtonBar Button:focus {
        background: $accent;
    }

    ButtonBar ProgressBar {
        margin: 1 5;
        width: 6fr;
    }

    ButtonBar Bar {
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
        """Create child widgets for the app."""
        yield Header()
        for value_name in self.values:
            yield ButtonBar(value_name)
        yield Footer()

    def key_left(self) -> None:
        bar_id = f"{self.focused.id}-bar"
        self.query_one(f"#{bar_id}").advance(-5)

    def key_right(self) -> None:
        bar_id = f"{self.focused.id}-bar"
        self.query_one(f"#{bar_id}").advance(+5)


if __name__ == "__main__":
    app = Valmix(["foo", "bar"])
    app.run()
