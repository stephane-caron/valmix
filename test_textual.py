from typing import List

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Widget
from textual.widgets import Button, Footer, Header, ProgressBar, RichLog


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
        width: 4fr;
    }

    ButtonBar Bar {
        width: 1fr;
    }

    """

    def __init__(self, label):
        self.label = label
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Button(self.label, id=self.label)
        yield ProgressBar(total=100, show_eta=False, id=f"{self.label}-bar")


class Valmix(App):

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    TITLE = "Valmix"

    def __init__(self, values: List[str]) -> None:
        self.values = values
        super().__init__()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        for value_name in self.values:
            yield ButtonBar(value_name)
        yield RichLog()
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(event)
        self.query_one(RichLog).write(self.focused.id)

    def key_left(self) -> None:
        bar_id = f"{self.focused.id}-bar"
        self.query_one(f"#{bar_id}").advance(-5)

    def key_right(self) -> None:
        bar_id = f"{self.focused.id}-bar"
        self.query_one(f"#{bar_id}").advance(+5)


if __name__ == "__main__":
    app = Valmix(["foo", "bar"])
    app.run()
