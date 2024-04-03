from typing import List

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.widgets import Button, Footer, Header, ProgressBar, RichLog


class Valmix(App):

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    CSS_PATH = "valmix.tcss"

    TITLE = "Valmix"

    def __init__(self, values: List[str]) -> None:
        self.values = values
        super().__init__()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Center():
            for value in self.values:
                yield Button(value, id=value)
                yield ProgressBar(total=100, show_eta=False, id=f"{value}-bar")
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
