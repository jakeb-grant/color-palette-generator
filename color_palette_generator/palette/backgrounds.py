from ..color import (
    create_color,
    adjust_color,
    clamp_saturation,
    contrast_ratio,
    hsl_to_rgb,
)
from ..constants import MAX_BG_SATURATION, MIN_TEXT_CONTRAST


# Target lightness ranges for themes
DARK_BG_MAX_LIGHTNESS = 18  # Dark themes: 8-18% lightness
DARK_BG_MIN_LIGHTNESS = 8
LIGHT_BG_MIN_LIGHTNESS = 85  # Light themes: 85-95% lightness
LIGHT_BG_MAX_LIGHTNESS = 95


def generate_background_colors(colors, is_dark_theme):
    """Generate background color variants.

    Returns dict with: background, background_medium, background_light, background_disabled,
    element, element_hover, element_active, element_selected, element_disabled
    """
    palette = {}

    if is_dark_theme:
        # Dark theme: pick a color with good saturation, then force it dark
        # Prefer colors with moderate saturation for character
        bg_base = sorted(colors, key=lambda c: abs(c.hsl[1] - 25))[0]
        h, s, lightness = bg_base.hsl
        # Clamp lightness to dark range
        target_l = min(max(lightness, DARK_BG_MIN_LIGHTNESS), DARK_BG_MAX_LIGHTNESS)
        # If the source color was bright, bring it down to dark range
        if lightness > DARK_BG_MAX_LIGHTNESS:
            target_l = DARK_BG_MAX_LIGHTNESS - 3  # Aim for ~15% lightness
        bg = create_color(*hsl_to_rgb(h, min(s, MAX_BG_SATURATION), target_l))
    else:
        # Light theme: pick a color with subtle saturation, then force it light
        bg_base = sorted(colors, key=lambda c: abs(c.hsl[1] - 15))[0]
        h, s, lightness = bg_base.hsl
        # Clamp lightness to light range
        target_l = min(max(lightness, LIGHT_BG_MIN_LIGHTNESS), LIGHT_BG_MAX_LIGHTNESS)
        # If the source color was dark, bring it up to light range
        if lightness < LIGHT_BG_MIN_LIGHTNESS:
            target_l = LIGHT_BG_MIN_LIGHTNESS + 5  # Aim for ~90% lightness
        bg = create_color(
            *hsl_to_rgb(h, min(s, MAX_BG_SATURATION / 2), target_l)
        )  # Lower saturation for light themes

    # Clamp background saturation to avoid gaudy
    bg = clamp_saturation(bg, MAX_BG_SATURATION)
    palette["background"] = bg

    # === BACKGROUND MEDIUM ===
    if is_dark_theme:
        bg_medium = adjust_color(bg, lightness_delta=4)
    else:
        bg_medium = adjust_color(bg, lightness_delta=-3)
    bg_medium = clamp_saturation(bg_medium, MAX_BG_SATURATION)
    palette["background_medium"] = bg_medium

    # === BACKGROUND LIGHT ===
    if is_dark_theme:
        bg_light = adjust_color(bg, lightness_delta=8)
    else:
        bg_light = adjust_color(bg, lightness_delta=-6)
    bg_light = clamp_saturation(bg_light, MAX_BG_SATURATION)
    palette["background_light"] = bg_light

    # === BACKGROUND DISABLED ===
    # Desaturated, slightly different from bg for disabled surfaces
    if is_dark_theme:
        bg_disabled = adjust_color(bg, lightness_delta=-2, saturation_delta=-10)
    else:
        bg_disabled = adjust_color(bg, lightness_delta=2, saturation_delta=-10)
    bg_disabled = clamp_saturation(bg_disabled, MAX_BG_SATURATION)
    palette["background_disabled"] = bg_disabled

    # === ELEMENT BACKGROUNDS ===
    # For interactive elements (buttons, inputs, checkboxes, etc.)
    if is_dark_theme:
        # element.background - sits between bg and bg_medium
        element_bg = adjust_color(bg, lightness_delta=2)
        # element.hover - lighter than element
        element_hover = adjust_color(bg, lightness_delta=5)
        # element.active - lighter than hover (pressed state)
        element_active = adjust_color(bg, lightness_delta=8)
        # element.selected - same as active
        element_selected = element_active
        # element.disabled - darker and desaturated
        element_disabled = adjust_color(bg, lightness_delta=-1, saturation_delta=-10)
    else:
        element_bg = adjust_color(bg, lightness_delta=-2)
        element_hover = adjust_color(bg, lightness_delta=-4)
        element_active = adjust_color(bg, lightness_delta=-6)
        element_selected = element_active
        element_disabled = adjust_color(bg, lightness_delta=2, saturation_delta=-10)

    palette["element"] = clamp_saturation(element_bg, MAX_BG_SATURATION)
    palette["element_hover"] = clamp_saturation(element_hover, MAX_BG_SATURATION)
    palette["element_active"] = clamp_saturation(element_active, MAX_BG_SATURATION)
    palette["element_selected"] = clamp_saturation(element_selected, MAX_BG_SATURATION)
    palette["element_disabled"] = clamp_saturation(element_disabled, MAX_BG_SATURATION)

    return palette


def ensure_background_contrast(palette, is_dark_theme):
    """Post-process backgrounds to ensure readable text is possible.

    For dark themes, if bg_light is too bright, we can't get enough contrast
    even with white text. This function darkens backgrounds if needed.

    Modifies palette in place.
    """
    bg = palette["background"]
    bg_light = palette["background_light"]

    if is_dark_theme:
        white_lum = 1.0
        max_possible_contrast = contrast_ratio(white_lum, bg_light.luminance)

        # If we can't even get MIN_TEXT_CONTRAST with white, darken the backgrounds
        if max_possible_contrast < MIN_TEXT_CONTRAST + 0.5:  # Add buffer
            # Calculate required bg_light luminance for 5.5:1 with white
            # contrast = (1 + 0.05) / (bg_lum + 0.05) >= 5.5
            # bg_lum <= (1.05 / 5.5) - 0.05 = 0.14
            target_lum = 0.12

            # Darken bg_light until we hit target luminance
            while bg_light.luminance > target_lum and bg_light.hsl[2] > 5:
                bg_light = adjust_color(bg_light, lightness_delta=-3)

            # Also darken main bg proportionally
            lum_diff = palette["background_light"].luminance - bg_light.luminance
            if lum_diff > 0:
                bg = adjust_color(bg, lightness_delta=-int(lum_diff * 80))
                bg = clamp_saturation(bg, MAX_BG_SATURATION)
                palette["background"] = bg

            palette["background_light"] = bg_light
