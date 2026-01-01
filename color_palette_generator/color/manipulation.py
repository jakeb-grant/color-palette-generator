from ..types import Color
from .conversion import rgb_to_hex, rgb_to_hsl, hsl_to_rgb


def relative_luminance(r, g, b):
    """Calculate relative luminance per WCAG 2.0"""

    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def create_color(r, g, b):
    """Create a Color namedtuple with all representations"""
    r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
    return Color(
        hex=rgb_to_hex(r, g, b),
        rgb=(r, g, b),
        hsl=rgb_to_hsl(r, g, b),
        luminance=relative_luminance(r, g, b),
    )


def adjust_color(color, lightness_delta=0, saturation_delta=0):
    """Adjust a color's HSL values"""
    h, s, lightness = color.hsl
    new_s = max(0, min(100, s + saturation_delta))
    new_l = max(0, min(100, lightness + lightness_delta))
    r, g, b = hsl_to_rgb(h, new_s, new_l)
    return create_color(r, g, b)


def set_color_lightness(color, target_lightness):
    """Set a color to a specific lightness"""
    h, s, _ = color.hsl
    r, g, b = hsl_to_rgb(h, s, target_lightness)
    return create_color(r, g, b)


def set_color_saturation(color, target_saturation):
    """Set a color to a specific saturation"""
    h, _, lightness = color.hsl
    r, g, b = hsl_to_rgb(h, target_saturation, lightness)
    return create_color(r, g, b)


def clamp_saturation(color, max_sat):
    """Reduce saturation if it exceeds max"""
    h, s, lightness = color.hsl
    if s > max_sat:
        r, g, b = hsl_to_rgb(h, max_sat, lightness)
        return create_color(r, g, b)
    return color


def blend_colors(color1, color2, factor):
    """Blend two colors together. factor=0 returns color1, factor=1 returns color2."""
    r1, g1, b1 = color1.rgb
    r2, g2, b2 = color2.rgb
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return create_color(r, g, b)


def is_accent_compatible(bg_color, accent_color, max_hue_diff=60, max_sat_diff=40):
    """Check if an accent color is close enough to blend with background for borders."""
    bg_h, bg_s, bg_l = bg_color.hsl
    acc_h, acc_s, acc_l = accent_color.hsl

    # Calculate hue difference (accounting for wraparound)
    hue_diff = abs(bg_h - acc_h)
    if hue_diff > 180:
        hue_diff = 360 - hue_diff

    # Check saturation difference
    sat_diff = abs(bg_s - acc_s)

    # Check lightness difference (accent shouldn't be extremely different)
    light_diff = abs(bg_l - acc_l)

    return hue_diff <= max_hue_diff and sat_diff <= max_sat_diff and light_diff <= 50
