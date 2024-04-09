from typing import List

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Center, VerticalScroll, Widget
from textual.widgets import Button, Footer, Header, ProgressBar, RichLog


class ButtonBar(Widget):

    DEFAULT_CSS = """
    ButtonBar {
    layout: horizontal;
    height: 3;
    }
    ButtonBar Button {
    width: 1fr;
    margin: 0 2;
    }
    ButtonBar ProgressBar {
    width: 4fr;
    margin: 1 5;
    }
    Bar {
    width: 2fr;
    height: 3;
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

    CSS_PATH = "valmix.tcss"

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
