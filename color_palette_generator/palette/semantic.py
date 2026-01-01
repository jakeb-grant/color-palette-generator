from ..color import create_color, ensure_terminal_contrast, hsl_to_rgb
from ..constants import MIN_SEMANTIC_CONTRAST


def generate_semantic_colors(palette, is_dark_theme):
    """Generate semantic colors (error, warning, success, info).

    Args:
        palette: Existing palette with backgrounds (modified in place)
        is_dark_theme: Whether this is a dark theme

    Adds to palette: error, warning, success, info
    """
    bg = palette["background"]
    bg_light = palette["background_light"]

    # Error - red
    error_base = create_color(*hsl_to_rgb(0, 65, 55))
    palette["error"] = ensure_terminal_contrast(
        error_base, bg, bg_light, MIN_SEMANTIC_CONTRAST, is_dark_theme
    )

    # Warning - yellow/orange
    warning_base = create_color(*hsl_to_rgb(38, 70, 55))
    palette["warning"] = ensure_terminal_contrast(
        warning_base, bg, bg_light, MIN_SEMANTIC_CONTRAST, is_dark_theme
    )

    # Success - green
    success_base = create_color(*hsl_to_rgb(120, 50, 45))
    palette["success"] = ensure_terminal_contrast(
        success_base, bg, bg_light, MIN_SEMANTIC_CONTRAST, is_dark_theme
    )

    # Info - cyan/blue
    info_base = create_color(*hsl_to_rgb(200, 60, 50))
    palette["info"] = ensure_terminal_contrast(
        info_base, bg, bg_light, MIN_SEMANTIC_CONTRAST, is_dark_theme
    )
