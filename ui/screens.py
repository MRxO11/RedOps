from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Static
from ui.widgets import OutputPanel

class MainScreen(Static):

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Static("Targets\n\n(active soon)", id="targets")
            yield OutputPanel(id="output")
        yield Input(placeholder="Enter command or: nmap <target>")
        yield Footer()
