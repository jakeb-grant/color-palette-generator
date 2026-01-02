"""Bridge between TUI state and existing palette generation."""

from ...types import Color
from ...palette import generate_functional_palette
from ...palette.backgrounds import generate_background_colors
from ...palette.foregrounds import generate_foreground_colors
from ...palette.accents import generate_accent_colors
from ...palette.semantic import generate_semantic_colors
from ...palette.terminal import generate_terminal_colors
from ...color import contrast_ratio


def generate_palette_from_selections(
    selected_colors: dict[str, Color],
    all_colors: list[Color],
    is_dark_theme: bool,
) -> dict[str, Color]:
    """Generate a full palette using user-selected colors as seeds.

    User can assign colors to key roles, and this function fills in
    the remaining roles using the existing generation logic.

    Args:
        selected_colors: User-assigned colors for key roles
        all_colors: Full list of extracted colors to use for generation
        is_dark_theme: Theme mode

    Returns:
        Complete palette dict
    """
    palette = dict(selected_colors)

    # Generate backgrounds if not user-assigned
    if "background" not in palette:
        bg_palette, _ = generate_background_colors(all_colors, is_dark_theme)
        for key in [
            "background",
            "background_medium",
            "background_light",
            "background_disabled",
            "element",
            "element_hover",
            "element_active",
            "element_selected",
            "element_disabled",
        ]:
            if key not in palette and key in bg_palette:
                palette[key] = bg_palette[key]

    # Generate foregrounds if not user-assigned
    if "foreground" not in palette:
        fg_palette = generate_foreground_colors(
            all_colors,
            palette["background"],
            palette.get("background_light", palette["background"]),
            is_dark_theme,
        )
        for key in [
            "foreground",
            "foreground_bright",
            "foreground_medium",
            "foreground_dim",
        ]:
            if key not in palette and key in fg_palette:
                palette[key] = fg_palette[key]

    # Generate accents if not user-assigned
    if "primary" not in palette:
        accent_palette = generate_accent_colors(
            all_colors,
            palette["background"],
            palette.get("background_light", palette["background"]),
            palette["foreground"],
            is_dark_theme,
        )
        for key in [
            "primary",
            "primary_variant",
            "secondary",
            "secondary_variant",
            "tertiary",
            "muted",
            "selection",
            "border",
            "border_variant",
            "border_focused",
            "border_selected",
            "border_disabled",
        ]:
            if key not in palette and key in accent_palette:
                palette[key] = accent_palette[key]

    # Generate semantic colors if not user-assigned
    semantic_keys = ["error", "warning", "success", "info"]
    if not any(key in palette for key in semantic_keys):
        semantic_palette = generate_semantic_colors(
            palette["background"],
            palette.get("background_light", palette["background"]),
            is_dark_theme,
        )
        for key in semantic_keys:
            if key not in palette and key in semantic_palette:
                palette[key] = semantic_palette[key]

    # Generate terminal colors if not present
    terminal_base = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    has_terminal = any(key in palette for key in terminal_base)
    if not has_terminal:
        terminal_palette = generate_terminal_colors(
            palette,
            all_colors,
            palette["background"],
            palette.get("background_light", palette["background"]),
            palette["foreground"],
            is_dark_theme,
        )
        for key in terminal_palette:
            if key not in palette:
                palette[key] = terminal_palette[key]

    return palette


def generate_full_palette_from_image(
    image_path: str,
    force_theme: str | None = None,
) -> tuple[dict[str, Color], list[Color], bool]:
    """Generate a complete palette from an image.

    Wrapper around the existing generate_functional_palette.

    Args:
        image_path: Path to source image
        force_theme: Optional theme mode ("dark" or "light")

    Returns:
        Tuple of (palette dict, extracted colors, is_dark_theme)
    """
    palette, colors, avg_color, is_dark = generate_functional_palette(
        image_path, force_theme
    )
    return palette, colors, is_dark


def calculate_all_contrasts(
    palette: dict[str, Color],
) -> dict[str, float]:
    """Calculate contrast ratios for all palette colors against background.

    Args:
        palette: Complete palette dict

    Returns:
        Dict of role_name -> contrast_ratio
    """
    if "background" not in palette:
        return {}

    bg = palette["background"]
    bg_light = palette.get("background_light", bg)

    ratios = {}
    for key, color in palette.items():
        if key.startswith("background") or key.startswith("element"):
            continue
        if key.startswith("_"):
            continue

        # Calculate against both backgrounds, use minimum
        ratio = contrast_ratio(color.luminance, bg.luminance)
        ratio_light = contrast_ratio(color.luminance, bg_light.luminance)
        ratios[key] = min(ratio, ratio_light)

    return ratios
