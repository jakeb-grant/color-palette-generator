"""Action bar widget with main action buttons."""

from textual.widgets import Button, Static
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.message import Message


class ActionBar(Horizontal):
    """Bottom action bar with main action buttons."""

    DEFAULT_CSS = """
    ActionBar {
        dock: bottom;
        height: 3;
        padding: 0 1;
        background: $surface;
        border-top: solid $primary;
    }
    ActionBar Button {
        margin: 0 1;
    }
    ActionBar .status {
        width: 1fr;
        text-align: right;
        padding: 0 2;
    }
    """

    use_real_colors: reactive[bool] = reactive(False)
    status_message: reactive[str] = reactive("")

    class GeneratePressed(Message):
        """Emitted when Generate button is pressed."""
        pass

    class SnapPressed(Message):
        """Emitted when Snap to Real button is pressed."""
        pass

    class ExportPressed(Message):
        """Emitted when Export button is pressed."""
        pass

    class HelpPressed(Message):
        """Emitted when Help button is pressed."""
        pass

    def compose(self):
        yield Button("Generate [g]", id="generate-btn", variant="primary")
        yield Button("Snap to Real [s]", id="snap-btn")
        yield Button("Export [e]", id="export-btn", variant="success")
        yield Button("? Help", id="help-btn")
        yield Static("", id="status", classes="status")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "generate-btn":
            self.post_message(self.GeneratePressed())
        elif button_id == "snap-btn":
            self.post_message(self.SnapPressed())
        elif button_id == "export-btn":
            self.post_message(self.ExportPressed())
        elif button_id == "help-btn":
            self.post_message(self.HelpPressed())

    def watch_use_real_colors(self, use_real: bool) -> None:
        """Update snap button appearance."""
        snap_btn = self.query_one("#snap-btn", Button)
        if use_real:
            snap_btn.label = "Using Real [s]"
            snap_btn.variant = "warning"
        else:
            snap_btn.label = "Snap to Real [s]"
            snap_btn.variant = "default"

    def watch_status_message(self, message: str) -> None:
        """Update status display."""
        status = self.query_one("#status", Static)
        status.update(message)

    def set_status(self, message: str) -> None:
        """Set status message."""
        self.status_message = message
