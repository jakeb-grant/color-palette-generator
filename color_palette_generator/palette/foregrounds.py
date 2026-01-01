from ..color import (
    adjust_color,
    clamp_saturation,
    ensure_contrast,
)
from ..constants import MAX_FG_SATURATION, MIN_TEXT_CONTRAST, MIN_DIM_CONTRAST


def generate_foreground_colors(colors, palette, is_dark_theme):
    """Generate foreground color variants.

    Args:
        colors: List of extracted colors sorted by luminance
        palette: Existing palette with backgrounds (modified in place)
        is_dark_theme: Whether this is a dark theme

    Adds to palette: foreground, foreground_bright, foreground_medium, foreground_dim
    """
    bg = palette["background"]
    bg_light = palette["background_light"]
    colors_by_lum = sorted(colors, key=lambda c: c.luminance)

    if is_dark_theme:
        # Start with lightest color from palette
        fg_candidates = [c for c in colors if c.luminance > 0.5]
        if fg_candidates:
            fg_base = sorted(fg_candidates, key=lambda c: c.luminance, reverse=True)[0]
        else:
            fg_base = colors_by_lum[-1]
        fg_base = adjust_color(fg_base, lightness_delta=10, saturation_delta=-20)
    else:
        # Light theme: dark foreground
        fg_candidates = [c for c in colors if c.luminance < 0.3]
        if fg_candidates:
            fg_base = sorted(fg_candidates, key=lambda c: c.luminance)[0]
        else:
            fg_base = colors_by_lum[0]
        fg_base = adjust_color(fg_base, lightness_delta=-10, saturation_delta=-20)

    # Clamp saturation and ensure contrast
    fg_base = clamp_saturation(fg_base, MAX_FG_SATURATION)
    fg = ensure_contrast(fg_base, bg, bg_light, MIN_TEXT_CONTRAST, is_dark_theme)

    # Push foreground a bit lighter for dark themes
    if is_dark_theme:
        fg = adjust_color(fg, lightness_delta=5)
    palette["foreground"] = fg

    # === FOREGROUND BRIGHT ===
    # Brighter than foreground for emphasis, headings, etc.
    if is_dark_theme:
        fg_bright_base = adjust_color(fg, lightness_delta=10)
    else:
        fg_bright_base = adjust_color(fg, lightness_delta=-10)
    fg_bright = clamp_saturation(fg_bright_base, MAX_FG_SATURATION)
    palette["foreground_bright"] = fg_bright

    # === FOREGROUND MEDIUM ===
    # Intermediate between foreground and foreground_dim
    if is_dark_theme:
        fg_medium_base = adjust_color(fg, lightness_delta=-3)
    else:
        fg_medium_base = adjust_color(fg, lightness_delta=4)
    fg_medium = ensure_contrast(
        fg_medium_base, bg, bg_light, MIN_TEXT_CONTRAST, is_dark_theme
    )
    palette["foreground_medium"] = fg_medium

    # === FOREGROUND DIM ===
    # Start closer to fg, then ensure contrast - don't go too far from readable
    if is_dark_theme:
        fg_dim_base = adjust_color(fg, lightness_delta=-8)
    else:
        fg_dim_base = adjust_color(fg, lightness_delta=10)
    fg_dim = ensure_contrast(fg_dim_base, bg, bg_light, MIN_DIM_CONTRAST, is_dark_theme)
    palette["foreground_dim"] = fg_dim
