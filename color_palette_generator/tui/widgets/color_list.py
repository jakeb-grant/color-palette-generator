"""Color list widget for displaying extracted colors."""

from textual.widgets import Static
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.message import Message

from ...types import Color
from .color_swatch import ColorSwatch


class ColorListView(VerticalScroll):
    """Scrollable list of extracted colors with selection support."""

    DEFAULT_CSS = ""

    colors: reactive[list[Color]] = reactive(list, always_update=True)
    selected_index: reactive[int | None] = reactive(None)
    role_assignments: reactive[dict[int, str]] = reactive(dict, always_update=True)

    class ColorSelected(Message):
        """Emitted when a color is selected."""

        def __init__(self, color: Color, index: int) -> None:
            self.color = color
            self.index = index
            super().__init__()

    def __init__(self, title: str = "Extracted Colors", **kwargs) -> None:
        super().__init__(**kwargs)
        self.title = title

    def compose(self):
        yield Static(self.title, classes="header")

    def watch_colors(self, colors: list[Color]) -> None:
        """Rebuild list when colors change."""
        self._rebuild_list()

    def watch_role_assignments(self, assignments: dict[int, str]) -> None:
        """Update role labels when assignments change."""
        self._rebuild_list()

    def _rebuild_list(self) -> None:
        """Rebuild the color swatch list."""
        # Remove existing swatches (keep header)
        for child in list(self.children):
            if isinstance(child, ColorSwatch):
                child.remove()

        # Sort colors by hue, then by luminance for better visual organization
        indexed_colors = list(enumerate(self.colors))
        indexed_colors.sort(key=lambda ic: (ic[1].hsl[0], ic[1].luminance))

        # Add new swatches (preserving original index for selection)
        for orig_index, color in indexed_colors:
            role = self.role_assignments.get(orig_index, "")
            swatch = ColorSwatch(
                color=color,
                role_name=role,
                index=orig_index,
                selected=(orig_index == self.selected_index),
            )
            self.mount(swatch)

    def on_color_swatch_selected(self, event: ColorSwatch.Selected) -> None:
        """Handle swatch selection."""
        self.selected_index = event.index

        # Update visual selection
        for child in self.children:
            if isinstance(child, ColorSwatch):
                child.selected = child.index == event.index

        # Propagate event up
        self.post_message(self.ColorSelected(event.color, event.index))

    def select_by_index(self, index: int) -> None:
        """Programmatically select a color by index."""
        if 0 <= index < len(self.colors):
            self.selected_index = index
            for child in self.children:
                if isinstance(child, ColorSwatch):
                    child.selected = child.index == index
