"""Centralized application state for the TUI."""

from dataclasses import dataclass, field
from typing import Optional

from ..types import Color


@dataclass
class AppState:
    """Centralized application state."""

    image_path: str = ""
    output_dir: str = ""
    theme_name: str = ""

    # Extracted colors from k-means
    extracted_colors: list[Color] = field(default_factory=list)

    # Real pixel colors (snapped from centroids)
    real_pixel_colors: list[Color] = field(default_factory=list)

    # Whether to use real pixel colors vs k-means centroids
    use_real_colors: bool = False

    # User-sampled colors (from clicking on image)
    sampled_colors: list[Color] = field(default_factory=list)

    # Role assignments: role_name -> color
    role_assignments: dict[str, Color] = field(default_factory=dict)

    # Currently selected color index (in active color list)
    selected_color_index: Optional[int] = None

    # Currently selected role for assignment
    selected_role: Optional[str] = None

    # Theme mode
    is_dark_theme: bool = True

    # Generated palette (full)
    palette: dict[str, Color] = field(default_factory=dict)

    # Blur opacity (None = auto-calculate)
    blur_opacity: Optional[float] = None

    @property
    def active_colors(self) -> list[Color]:
        """Get the currently active color list (real or k-means)."""
        if self.use_real_colors and self.real_pixel_colors:
            return self.real_pixel_colors
        return self.extracted_colors

    @property
    def all_available_colors(self) -> list[Color]:
        """Get all colors available for selection (extracted + sampled)."""
        return self.active_colors + self.sampled_colors


# Standard palette roles grouped by category
ROLE_GROUPS = {
    "Backgrounds": [
        "background",
        "background_medium",
        "background_light",
        "background_disabled",
    ],
    "Elements": [
        "element",
        "element_hover",
        "element_active",
        "element_selected",
        "element_disabled",
    ],
    "Foregrounds": [
        "foreground",
        "foreground_bright",
        "foreground_medium",
        "foreground_dim",
    ],
    "Accents": [
        "primary",
        "primary_variant",
        "secondary",
        "secondary_variant",
        "tertiary",
        "muted",
        "selection",
    ],
    "Borders": [
        "border",
        "border_variant",
        "border_focused",
        "border_selected",
        "border_disabled",
    ],
    "Semantic": [
        "error",
        "warning",
        "success",
        "info",
    ],
    "ANSI Colors": [
        "black",
        "black_bright",
        "black_dim",
        "red",
        "red_bright",
        "red_dim",
        "green",
        "green_bright",
        "green_dim",
        "yellow",
        "yellow_bright",
        "yellow_dim",
        "blue",
        "blue_bright",
        "blue_dim",
        "magenta",
        "magenta_bright",
        "magenta_dim",
        "cyan",
        "cyan_bright",
        "cyan_dim",
        "white",
        "white_bright",
        "white_dim",
    ],
}

# Contrast requirements for each role
ROLE_CONTRAST_REQUIREMENTS = {
    "foreground": 5.0,
    "foreground_bright": 5.0,
    "foreground_medium": 4.5,
    "foreground_dim": 4.0,
    "primary": 4.0,
    "primary_variant": 3.0,
    "secondary": 4.0,
    "secondary_variant": 3.0,
    "tertiary": 4.5,
    "error": 4.5,
    "warning": 4.5,
    "success": 4.5,
    "info": 4.5,
    # ANSI colors
    "red": 4.5,
    "red_bright": 4.5,
    "red_dim": 3.0,
    "green": 4.5,
    "green_bright": 4.5,
    "green_dim": 3.0,
    "yellow": 4.5,
    "yellow_bright": 4.5,
    "yellow_dim": 3.0,
    "blue": 4.5,
    "blue_bright": 4.5,
    "blue_dim": 3.0,
    "magenta": 4.5,
    "magenta_bright": 4.5,
    "magenta_dim": 3.0,
    "cyan": 4.5,
    "cyan_bright": 4.5,
    "cyan_dim": 3.0,
    "white": 4.5,
    "white_bright": 4.5,
    "white_dim": 3.0,
    "black_bright": 3.0,
    "black_dim": 2.0,
}

# ANSI color families (base name -> can derive bright/dim variants)
ANSI_FAMILIES = ["red", "green", "yellow", "blue", "magenta", "cyan", "black", "white"]

# Role families that can be derived from a base color
DERIVABLE_GROUPS = {
    "background": ["background", "background_medium", "background_light", "background_disabled"],
    "element": ["element", "element_hover", "element_active", "element_selected", "element_disabled"],
    "foreground": ["foreground", "foreground_bright", "foreground_medium", "foreground_dim"],
    "border": ["border", "border_variant", "border_focused", "border_selected", "border_disabled"],
}
