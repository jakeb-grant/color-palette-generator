from ..color import create_color, contrast_ratio
from ..constants import MIN_DIM_CONTRAST


def opacity_to_hex(opacity):
    """Convert 0.0-1.0 opacity to hex string (00-ff)."""
    clamped = max(0.0, min(1.0, opacity))
    return f"{int(clamped * 255):02x}"


def blend_color_with_opacity(bg_color, wallpaper_rgb, opacity):
    """
    Calculate the blended color when bg_color is shown at given opacity over wallpaper.
    Returns a new Color with the blended RGB values.
    """
    bg_r, bg_g, bg_b = bg_color.rgb
    wp_r, wp_g, wp_b = wallpaper_rgb

    blended_r = int(bg_r * opacity + wp_r * (1 - opacity))
    blended_g = int(bg_g * opacity + wp_g * (1 - opacity))
    blended_b = int(bg_b * opacity + wp_b * (1 - opacity))

    return create_color(blended_r, blended_g, blended_b)


def calculate_safe_opacity(bg_color, fg_color, min_contrast, is_dark_theme):
    """
    Calculate the minimum opacity that maintains contrast with worst-case wallpaper.

    For dark themes: worst case is white wallpaper (#ffffff)
    For light themes: worst case is black wallpaper (#000000)

    Uses binary search to find the minimum opacity where:
        contrast(blended_bg, fg) >= min_contrast

    Returns opacity value 0.0-1.0 (higher = more opaque)
    """
    # Worst case wallpaper
    wallpaper_rgb = (255, 255, 255) if is_dark_theme else (0, 0, 0)

    low, high = 0.0, 1.0
    result = 1.0  # Default to fully opaque if we can't find a solution

    for _ in range(50):  # Binary search iterations
        mid = (low + high) / 2

        blended = blend_color_with_opacity(bg_color, wallpaper_rgb, mid)
        achieved_contrast = contrast_ratio(blended.luminance, fg_color.luminance)

        if achieved_contrast >= min_contrast:
            result = mid
            high = mid  # Try for more transparency (lower opacity)
        else:
            low = mid  # Need more opacity

        if high - low < 0.001:
            break

    return result


def calculate_theme_opacity(palette, is_dark_theme):
    """
    Calculate optimal opacity for a theme based on contrast preservation.
    Uses the lowest-contrast text (foreground_dim) to ensure all text remains readable.

    Returns opacity value 0.0-1.0
    """
    bg = palette["background"]
    fg_dim = palette["foreground_dim"]

    # Use MIN_DIM_CONTRAST as the threshold since that's our lowest acceptable contrast
    opacity = calculate_safe_opacity(bg, fg_dim, MIN_DIM_CONTRAST, is_dark_theme)

    # Add a small safety margin (5% more opaque)
    opacity = min(1.0, opacity + 0.05)

    return opacity


def calculate_layered_opacities(editor_target):
    """
    Calculate opacity values for the layered transparency system.

    The hierarchy (dark theme, darkest to lightest):
    - Editor area = most opaque (editor_target)
    - Panels = medium (global background alone)
    - Title/status bars = lightest (5% more transparent than editor)

    Stacking: editor_target = global + editor_layer * (1 - global)

    Returns dict with opacity values (0.0-1.0) for each layer.
    """
    # Global background (panels) is 95% of editor target (5% more transparent)
    global_opacity = editor_target * 0.95

    # Editor layer combines with global to reach editor_target
    # editor_target = global + editor_layer * (1 - global)
    # editor_layer = (editor_target - global) / (1 - global)
    if global_opacity < 1.0:
        editor_layer = (editor_target - global_opacity) / (1 - global_opacity)
    else:
        editor_layer = 0.0

    # Title/status bars are 5% more transparent than editor target (standalone)
    title_status_opacity = editor_target * 0.95

    # Tab bar stacks on global, should match editor combined opacity
    # So tab_bar_layer uses same calculation as editor_layer
    tab_bar_layer = editor_layer

    return {
        "global": global_opacity,  # background (panels inherit this)
        "editor_layer": editor_layer,  # editor.background, editor.gutter.background
        "tab_bar_layer": tab_bar_layer,  # tab_bar.background
        "tab_layer": editor_layer
        * 0.5,  # tab.active/inactive (50% of editor layer for subtlety)
        "title_status": title_status_opacity,  # title_bar, status_bar (standalone)
        "transparent": 0.0,  # panel, terminal, surface (fully transparent)
    }
