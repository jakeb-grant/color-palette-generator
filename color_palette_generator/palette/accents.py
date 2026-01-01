from ..color import (
    create_color,
    adjust_color,
    clamp_saturation,
    blend_colors,
    is_accent_compatible,
    ensure_terminal_contrast,
    hsl_to_rgb,
)
from ..constants import MAX_ACCENT_SATURATION, MIN_SEMANTIC_CONTRAST


def generate_accent_colors(colors, palette, is_dark_theme):
    """Generate accent, border, and selection colors.

    Args:
        colors: List of extracted colors
        palette: Existing palette with backgrounds (modified in place)
        is_dark_theme: Whether this is a dark theme

    Adds to palette: primary, primary_variant, secondary, secondary_variant,
    tertiary, muted, selection, border, border_variant, border_focused,
    border_selected, border_disabled
    """
    bg = palette["background"]
    bg_light = palette["background_light"]
    colors_by_sat = sorted(colors, key=lambda c: c.hsl[1], reverse=True)

    # === PRIMARY ACCENT ===
    vibrant_colors = [c for c in colors if c.hsl[1] > 35 and 0.1 < c.luminance < 0.75]
    if vibrant_colors:
        primary = sorted(vibrant_colors, key=lambda c: c.hsl[1], reverse=True)[0]
    else:
        primary = colors_by_sat[0]
    primary = clamp_saturation(primary, MAX_ACCENT_SATURATION)
    palette["primary"] = primary

    # === SECONDARY ACCENT ===
    primary_hue = primary.hsl[0]
    secondary_candidates = [
        c
        for c in colors
        if c.hsl[1] > 25
        and abs(c.hsl[0] - primary_hue) > 40
        and 0.1 < c.luminance < 0.75
    ]
    if secondary_candidates:
        secondary = sorted(secondary_candidates, key=lambda c: c.hsl[1], reverse=True)[
            0
        ]
    else:
        comp_hue = (primary_hue + 150) % 360
        r, g, b = hsl_to_rgb(comp_hue, min(primary.hsl[1], 60), 50)
        secondary = create_color(r, g, b)
    secondary = clamp_saturation(secondary, MAX_ACCENT_SATURATION)
    palette["secondary"] = secondary

    # === PRIMARY VARIANT ===
    # Lighter/darker version of primary for hover states, borders, etc.
    if is_dark_theme:
        primary_variant = adjust_color(primary, lightness_delta=15, saturation_delta=-5)
    else:
        primary_variant = adjust_color(
            primary, lightness_delta=-15, saturation_delta=-5
        )
    primary_variant = clamp_saturation(primary_variant, MAX_ACCENT_SATURATION)
    palette["primary_variant"] = primary_variant

    # === SECONDARY VARIANT ===
    # Lighter/darker version of secondary
    if is_dark_theme:
        secondary_variant = adjust_color(
            secondary, lightness_delta=15, saturation_delta=-5
        )
    else:
        secondary_variant = adjust_color(
            secondary, lightness_delta=-15, saturation_delta=-5
        )
    secondary_variant = clamp_saturation(secondary_variant, MAX_ACCENT_SATURATION)
    palette["secondary_variant"] = secondary_variant

    # === TERTIARY ===
    # High-contrast highlight color for syntax, links, accents
    tertiary_hue = (primary_hue + 80) % 360
    tertiary_candidates = [
        c for c in colors if abs(c.hsl[0] - tertiary_hue) < 50 and c.hsl[1] > 20
    ]
    if tertiary_candidates:
        tertiary_base = tertiary_candidates[0]
    else:
        r, g, b = hsl_to_rgb(tertiary_hue, 50, 55)
        tertiary_base = create_color(r, g, b)
    tertiary_base = clamp_saturation(tertiary_base, MAX_ACCENT_SATURATION)
    # Enforce contrast for readability as highlight/accent text
    tertiary = ensure_terminal_contrast(
        tertiary_base, bg, bg_light, MIN_SEMANTIC_CONTRAST, is_dark_theme
    )
    palette["tertiary"] = tertiary

    # === MUTED ===
    muted = adjust_color(
        bg, lightness_delta=-5 if is_dark_theme else 5, saturation_delta=-5
    )
    palette["muted"] = muted

    # === SELECTION ===
    selection = adjust_color(primary, lightness_delta=-15, saturation_delta=-25)
    palette["selection"] = selection

    # === BORDER COLORS ===
    _generate_border_colors(palette, is_dark_theme)


def _generate_border_colors(palette, is_dark_theme):
    """Generate border color variants. Modifies palette in place."""
    bg = palette["background"]
    bg_light = palette["background_light"]
    primary = palette["primary"]
    secondary = palette["secondary"]
    secondary_variant = palette["secondary_variant"]

    # Borders should be subtle - close to background but with a hint of accent if compatible
    BORDER_BLEND_COMPATIBLE = 0.50  # Blend toward accent if compatible
    BORDER_BLEND_INCOMPATIBLE = 0.05  # Very subtle blend even if incompatible

    if is_dark_theme:
        # Dark mode: borders slightly lighter than background_light
        border_base = adjust_color(bg_light, lightness_delta=5)
    else:
        # Light mode: borders slightly darker than background
        border_base = adjust_color(bg, lightness_delta=-5)

    # Check if primary accent is compatible for blending
    if is_accent_compatible(bg, primary):
        blend_factor = BORDER_BLEND_COMPATIBLE
    else:
        blend_factor = BORDER_BLEND_INCOMPATIBLE

    border = blend_colors(border_base, primary, blend_factor)
    border_variant = blend_colors(
        adjust_color(border_base, lightness_delta=3 if is_dark_theme else -3),
        primary,
        blend_factor * 0.7,
    )

    palette["border"] = border
    palette["border_variant"] = border_variant

    # Focused/selected borders can be more prominent - use secondary with some blending
    if is_accent_compatible(bg, secondary):
        focus_blend = BORDER_BLEND_COMPATIBLE
    else:
        focus_blend = BORDER_BLEND_INCOMPATIBLE

    border_focused = blend_colors(border_base, secondary, focus_blend * 1.2)
    border_selected = blend_colors(border_base, secondary_variant, focus_blend)

    palette["border_focused"] = border_focused
    palette["border_selected"] = border_selected

    # Disabled border - very muted
    palette["border_disabled"] = adjust_color(
        border_base, lightness_delta=-3 if is_dark_theme else 3, saturation_delta=-10
    )
