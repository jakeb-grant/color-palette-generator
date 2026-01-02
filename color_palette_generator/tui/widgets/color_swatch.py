"""Color swatch widget for displaying a single color."""

from textual.widgets import Static
from textual.reactive import reactive
from textual.message import Message

from ...types import Color


class ColorSwatch(Static):
    """Displays a single color with selection state and optional role label."""

    DEFAULT_CSS = ""

    color: reactive[Color | None] = reactive(None)
    selected: reactive[bool] = reactive(False)
    role_name: reactive[str] = reactive("")
    index: reactive[int] = reactive(-1)

    class Selected(Message):
        """Emitted when swatch is clicked."""

        def __init__(self, color: Color, index: int) -> None:
            self.color = color
            self.index = index
            super().__init__()

    def __init__(
        self,
        color: Color | None = None,
        role_name: str = "",
        index: int = -1,
        selected: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.color = color
        self.role_name = role_name
        self.index = index
        self.selected = selected

    def render(self) -> str:
        if not self.color:
            return "[dim]No color[/]"

        # Build the display string
        hex_code = self.color.hex
        role_indicator = f" [dim]({self.role_name})[/]" if self.role_name else ""
        select_marker = "[bold]>[/] " if self.selected else "  "

        # Use Rich markup to show color block
        return f"{select_marker}[on {hex_code}]  [/] {hex_code}{role_indicator}"

    def watch_selected(self, selected: bool) -> None:
        """Update CSS class when selection changes."""
        self.set_class(selected, "selected")

    def on_click(self) -> None:
        """Handle click events."""
        if self.color:
            self.post_message(self.Selected(self.color, self.index))
