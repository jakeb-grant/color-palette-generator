"""Help screen modal showing keybindings and usage instructions."""

from textual.screen import ModalScreen
from textual.widgets import Button, Static
from textual.containers import Vertical, VerticalScroll
from textual.binding import Binding


class HelpScreen(ModalScreen):
    """Modal dialog showing help and keybindings."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("?", "dismiss", "Close"),
    ]

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }

    #help-dialog {
        width: 70;
        height: auto;
        max-height: 40;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #help-dialog .title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #help-content {
        height: auto;
        max-height: 32;
        margin: 1 0;
    }

    #help-dialog .section {
        margin-top: 1;
        text-style: bold;
        color: $primary;
    }

    #help-dialog .keys {
        margin-left: 2;
    }

    #help-dialog .close-btn {
        margin-top: 1;
        width: 100%;
    }
    """

    HELP_TEXT = """[bold cyan]━━━ Workflow ━━━[/]

[dim]1.[/] [bold]Select a color[/] from Extracted Colors (top right)
   Click any color swatch to select it

[dim]2.[/] [bold]Assign to role[/] in Role Assignments (bottom right)
   Click a role to assign the selected color

[dim]3.[/] [bold]Sample from image[/] (top left)
   Click anywhere on the image to sample a color

[dim]4.[/] [bold]Adjust ANSI colors[/]
   Select a color → select ANSI role → press [bold]d[/] to derive family

[bold cyan]━━━ General ━━━[/]

  [bold]?[/]         Show this help
  [bold]q[/]         Quit
  [bold]n[/]         Load new image
  [bold]g[/]         Regenerate palette
  [bold]t[/]         Toggle dark/light theme
  [bold]s[/]         Toggle snap-to-real colors
  [bold]e[/]         Export palette
  [bold]f[/]         Fix contrast (auto-adjust for readability)
  [bold]r[/]         Restore role to original color
  [bold]Enter[/]     Assign selected color to role
  [bold]Escape[/]    Clear selection

[bold cyan]━━━ Derive Families (select color + role, press d) ━━━[/]

  [bold]Backgrounds[/]  background → medium, light, disabled
  [bold]Elements[/]     element → hover, active, selected, disabled
  [bold]Foregrounds[/]  foreground → bright, medium, dim
  [bold]Borders[/]      border → variant, focused, selected, disabled
  [bold]ANSI Colors[/]  red/green/etc → bright, dim

[bold cyan]━━━ Opacity ━━━[/]

  [bold]o / O[/]     Decrease / Increase blur opacity (±5%)

[bold cyan]━━━ HSL Nudging (select a role first) ━━━[/]

  [bold]h / H[/]     Decrease / Increase hue (±10)
  [bold][ / ][/]     Decrease / Increase saturation (±5)
  [bold]l / L[/]     Decrease / Increase lightness (±5)

  [dim]Adjusting a base ANSI color auto-updates its variants[/]

[bold cyan]━━━ Panels ━━━[/]

  [bold]Top Left[/]      Image preview (click to sample)
  [bold]Top Right[/]     Extracted colors (click to select)
  [bold]Bottom Left[/]   Contrast report (WCAG compliance)
  [bold]Bottom Right[/]  Role assignments (click to assign)
"""

    def compose(self):
        with Vertical(id="help-dialog"):
            yield Static("[bold]Color Palette Generator - Help[/]", classes="title")
            with VerticalScroll(id="help-content"):
                yield Static(self.HELP_TEXT)
            yield Button("Close [?]", id="close-btn", variant="primary", classes="close-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle close button."""
        if event.button.id == "close-btn":
            self.dismiss()

    def action_dismiss(self) -> None:
        """Dismiss the help screen."""
        self.dismiss()
