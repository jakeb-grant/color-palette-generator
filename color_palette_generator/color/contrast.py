from .manipulation import adjust_color


def contrast_ratio(lum1, lum2):
    """Calculate contrast ratio between two luminances"""
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def ensure_contrast(color, bg_color, bg_light_color, min_contrast, is_dark_theme):
    """
    Adjust color to ensure it meets minimum contrast against BOTH backgrounds.
    Returns adjusted color.
    """
    max_iterations = 50
    step = 3 if is_dark_theme else -3

    current = color
    for _ in range(max_iterations):
        contrast_bg = contrast_ratio(current.luminance, bg_color.luminance)
        contrast_bg_light = contrast_ratio(current.luminance, bg_light_color.luminance)
        min_achieved = min(contrast_bg, contrast_bg_light)

        if min_achieved >= min_contrast:
            return current

        # Adjust lightness in the appropriate direction
        current = adjust_color(current, lightness_delta=step)

        # Clamp to avoid going too far
        if current.hsl[2] > 95 or current.hsl[2] < 5:
            break

    return current


def ensure_terminal_contrast(
    color, bg_color, bg_light_color, min_contrast, is_dark_theme
):
    """
    Adjust terminal color for readability. More aggressive than text.
    """
    max_iterations = 60
    step = 4 if is_dark_theme else -4

    current = color
    for _ in range(max_iterations):
        contrast_bg = contrast_ratio(current.luminance, bg_color.luminance)
        contrast_bg_light = contrast_ratio(current.luminance, bg_light_color.luminance)
        min_achieved = min(contrast_bg, contrast_bg_light)

        if min_achieved >= min_contrast:
            return current

        current = adjust_color(current, lightness_delta=step)

        if current.hsl[2] > 90 or current.hsl[2] < 10:
            break

    return current
