"""Role panel widget for displaying and assigning palette roles."""

from textual.widgets import Static
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.message import Message

from ...types import Color
from ..state import ROLE_GROUPS, ROLE_CONTRAST_REQUIREMENTS


class RoleSlot(Static):
    """A single role slot that can receive a color assignment."""

    DEFAULT_CSS = ""

    role_name: reactive[str] = reactive("")
    assigned_color: reactive[Color | None] = reactive(None)
    contrast_ratio: reactive[float] = reactive(0.0)
    required_contrast: reactive[float] = reactive(4.5)
    selected: reactive[bool] = reactive(False)

    class RoleSelected(Message):
        """Emitted when role slot is clicked."""

        def __init__(self, role_name: str) -> None:
            self.role_name = role_name
            super().__init__()

    class RoleCleared(Message):
        """Emitted when role assignment is cleared (double-click or key)."""

        def __init__(self, role_name: str) -> None:
            self.role_name = role_name
            super().__init__()

    def __init__(self, role_name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.role_name = role_name
        self.required_contrast = ROLE_CONTRAST_REQUIREMENTS.get(role_name, 4.0)

    def render(self) -> str:
        select_marker = "[bold]>[/] " if self.selected else "  "

        if self.assigned_color:
            hex_code = self.assigned_color.hex
            # Show contrast if applicable
            if self.contrast_ratio > 0:
                meets_req = self.contrast_ratio >= self.required_contrast
                status = "[green]✓[/]" if meets_req else "[red]✗[/]"
                contrast_str = f" {self.contrast_ratio:.1f}:1 {status}"
            else:
                contrast_str = ""

            return (
                f"{select_marker}[dim]{self.role_name}:[/] "
                f"[on {hex_code}]  [/] {hex_code}{contrast_str}"
            )
        else:
            return f"{select_marker}[dim]{self.role_name}:[/] [dim italic]click to assign[/]"

    def watch_selected(self, selected: bool) -> None:
        """Update CSS class when selection changes."""
        self.set_class(selected, "selected")

    def watch_assigned_color(self, color: Color | None) -> None:
        """Update CSS class when color is assigned."""
        self.set_class(color is not None, "assigned")

    def watch_contrast_ratio(self, ratio: float) -> None:
        """Update CSS class based on contrast."""
        fails = ratio > 0 and ratio < self.required_contrast
        self.set_class(fails, "contrast-fail")

    def on_click(self) -> None:
        """Handle click events."""
        self.post_message(self.RoleSelected(self.role_name))


class RolePanel(VerticalScroll):
    """Scrollable panel showing all palette roles grouped by category."""

    DEFAULT_CSS = ""

    role_assignments: reactive[dict[str, Color]] = reactive(dict, always_update=True)
    contrast_ratios: reactive[dict[str, float]] = reactive(dict, always_update=True)
    selected_role: reactive[str | None] = reactive(None)

    class RoleSelected(Message):
        """Emitted when a role is selected."""

        def __init__(self, role_name: str) -> None:
            self.role_name = role_name
            super().__init__()

    def compose(self):
        yield Static("[bold]Role Assignments[/]", classes="title")

        for group_name, roles in ROLE_GROUPS.items():
            yield Static(f"[dim]{group_name}[/]", classes="group-header")
            for role in roles:
                yield RoleSlot(role_name=role, id=f"role-{role}")

    def watch_role_assignments(self, assignments: dict[str, Color]) -> None:
        """Update role slots when assignments change."""
        for role_name, color in assignments.items():
            try:
                slot = self.query_one(f"#role-{role_name}", RoleSlot)
                if slot:
                    slot.assigned_color = color
            except Exception:
                # Role not in ROLE_GROUPS, skip
                pass

    def watch_contrast_ratios(self, ratios: dict[str, float]) -> None:
        """Update contrast displays."""
        for role_name, ratio in ratios.items():
            try:
                slot = self.query_one(f"#role-{role_name}", RoleSlot)
                if slot:
                    slot.contrast_ratio = ratio
            except Exception:
                pass

    def watch_selected_role(self, role: str | None) -> None:
        """Update visual selection."""
        for child in self.query(RoleSlot):
            child.selected = child.role_name == role

    def on_role_slot_role_selected(self, event: RoleSlot.RoleSelected) -> None:
        """Handle role slot selection."""
        self.selected_role = event.role_name
        self.post_message(self.RoleSelected(event.role_name))
