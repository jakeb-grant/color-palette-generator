"""Contrast report widget for displaying WCAG contrast ratios."""

from textual.widgets import Static
from textual.containers import VerticalScroll
from textual.reactive import reactive

from ...types import Color
from ...color import contrast_ratio
from ..state import ROLE_CONTRAST_REQUIREMENTS


# All foreground/text roles to check contrast for
CONTRAST_CHECK_ROLES = [
    # Foregrounds
    ("foreground", "fg", 5.0),
    ("foreground_bright", "fg_brt", 5.0),
    ("foreground_medium", "fg_med", 4.5),
    ("foreground_dim", "fg_dim", 4.0),
    # Accents
    ("primary", "primary", 4.0),
    ("primary_variant", "pri_var", 3.0),
    ("secondary", "second", 4.0),
    ("secondary_variant", "sec_var", 3.0),
    ("tertiary", "tertiary", 4.5),
    # Semantic
    ("error", "error", 4.5),
    ("warning", "warning", 4.5),
    ("success", "success", 4.5),
    ("info", "info", 4.5),
    # ANSI colors
    ("red", "red", 4.5),
    ("red_bright", "red_brt", 4.5),
    ("red_dim", "red_dim", 3.0),
    ("green", "green", 4.5),
    ("green_bright", "grn_brt", 4.5),
    ("green_dim", "grn_dim", 3.0),
    ("yellow", "yellow", 4.5),
    ("yellow_bright", "yel_brt", 4.5),
    ("yellow_dim", "yel_dim", 3.0),
    ("blue", "blue", 4.5),
    ("blue_bright", "blu_brt", 4.5),
    ("blue_dim", "blu_dim", 3.0),
    ("magenta", "magenta", 4.5),
    ("magenta_bright", "mag_brt", 4.5),
    ("magenta_dim", "mag_dim", 3.0),
    ("cyan", "cyan", 4.5),
    ("cyan_bright", "cyn_brt", 4.5),
    ("cyan_dim", "cyn_dim", 3.0),
    ("white", "white", 4.5),
    ("white_bright", "wht_brt", 4.5),
    ("white_dim", "wht_dim", 3.0),
    ("black_bright", "blk_brt", 3.0),
    ("black_dim", "blk_dim", 2.0),
]


class ContrastReport(VerticalScroll):
    """Live contrast report for current palette assignments."""

    DEFAULT_CSS = ""

    palette: reactive[dict[str, Color]] = reactive(dict, always_update=True)
    is_dark_theme: reactive[bool] = reactive(True)

    def compose(self):
        yield Static("[bold]Contrast Report[/]", classes="header")

    def watch_palette(self, palette: dict[str, Color]) -> None:
        """Rebuild report when palette changes."""
        self._rebuild_report()

    def _rebuild_report(self) -> None:
        """Rebuild the contrast report."""
        # Remove old entries (keep header)
        for child in list(self.children):
            if not child.has_class("header"):
                child.remove()

        if not self.palette or "background" not in self.palette:
            self.mount(Static("[dim]No palette loaded[/]"))
            return

        bg = self.palette["background"]
        bg_light = self.palette.get("background_light", bg)

        all_pass = True
        for role, short_name, required in CONTRAST_CHECK_ROLES:
            if role not in self.palette:
                continue

            color = self.palette[role]
            ratio = contrast_ratio(color.luminance, bg.luminance)
            ratio_light = contrast_ratio(color.luminance, bg_light.luminance)

            min_ratio = min(ratio, ratio_light)
            passes = min_ratio >= required

            if passes:
                status = "[green]✓[/]"
            else:
                status = "[red]✗[/]"
                all_pass = False

            hex_code = color.hex
            line = f"[on {hex_code}]  [/] {short_name:8} {min_ratio:4.1f}:1 {status}"
            self.mount(Static(line))

        # Summary
        self.mount(Static(""))
        if all_pass:
            self.mount(Static("[green]All pass WCAG[/]", classes="pass"))
        else:
            self.mount(Static("[red]Some fail contrast[/]", classes="fail"))

    def get_contrast_ratios(self) -> dict[str, float]:
        """Calculate contrast ratios for all roles."""
        ratios = {}

        if not self.palette or "background" not in self.palette:
            return ratios

        bg = self.palette["background"]
        bg_light = self.palette.get("background_light", bg)

        for role in ROLE_CONTRAST_REQUIREMENTS:
            if role in self.palette:
                color = self.palette[role]
                ratio = contrast_ratio(color.luminance, bg.luminance)
                ratio_light = contrast_ratio(color.luminance, bg_light.luminance)
                ratios[role] = min(ratio, ratio_light)

        return ratios
