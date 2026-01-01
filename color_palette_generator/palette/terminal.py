from ..color import (
    create_color,
    adjust_color,
    ensure_terminal_contrast,
    hsl_to_rgb,
)
from ..constants import MIN_TERMINAL_CONTRAST


def generate_terminal_colors(colors, palette, is_dark_theme):
    """Generate 24 terminal colors (base, bright, dim for each of 8 colors).

    Args:
        colors: List of extracted colors
        palette: Existing palette with backgrounds, foregrounds, and semantic colors
                (modified in place)
        is_dark_theme: Whether this is a dark theme

    Adds to palette: black, black_bright, black_dim, red, red_bright, red_dim,
    green, green_bright, green_dim, yellow, yellow_bright, yellow_dim,
    blue, blue_bright, blue_dim, magenta, magenta_bright, magenta_dim,
    cyan, cyan_bright, cyan_dim, white, white_bright, white_dim
    """
    bg = palette["background"]
    bg_light = palette["background_light"]
    fg = palette["foreground"]
    fg_dim = palette["foreground_dim"]

    # === BLACK ===
    # Black should always be dark, desaturated to ensure pure gray tones
    if is_dark_theme:
        black_lightness = bg.hsl[2]
        palette["black"] = create_color(*hsl_to_rgb(0, 0, black_lightness))
        # Cap black_bright at 40% to stay distinct from white (which starts at ~60%)
        palette["black_bright"] = create_color(*hsl_to_rgb(0, 0, min(40, black_lightness + 20)))
        palette["black_dim"] = create_color(*hsl_to_rgb(0, 0, max(3, black_lightness - 8)))
    else:
        black_lightness = fg.hsl[2]
        palette["black"] = create_color(*hsl_to_rgb(0, 0, black_lightness))
        palette["black_bright"] = create_color(*hsl_to_rgb(0, 0, min(30, black_lightness + 8)))
        palette["black_dim"] = create_color(*hsl_to_rgb(0, 0, min(35, black_lightness + 12)))
        # For light themes, ensure black variants meet contrast
        palette["black_bright"] = ensure_terminal_contrast(
            palette["black_bright"], bg, bg_light, MIN_TERMINAL_CONTRAST, is_dark_theme
        )

    # === RED ===
    palette["red"] = palette["error"]
    palette["red_bright"] = ensure_terminal_contrast(
        adjust_color(palette["error"], lightness_delta=12),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )
    palette["red_dim"] = ensure_terminal_contrast(
        adjust_color(
            palette["error"],
            lightness_delta=-15 if is_dark_theme else 12,
            saturation_delta=-10,
        ),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )

    # === GREEN ===
    palette["green"] = palette["success"]
    palette["green_bright"] = ensure_terminal_contrast(
        adjust_color(palette["success"], lightness_delta=15),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )
    palette["green_dim"] = ensure_terminal_contrast(
        adjust_color(
            palette["success"],
            lightness_delta=-15 if is_dark_theme else 12,
            saturation_delta=-10,
        ),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )

    # === YELLOW ===
    palette["yellow"] = palette["warning"]
    palette["yellow_bright"] = ensure_terminal_contrast(
        adjust_color(palette["warning"], lightness_delta=12),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )
    palette["yellow_dim"] = ensure_terminal_contrast(
        adjust_color(
            palette["warning"],
            lightness_delta=-15 if is_dark_theme else 12,
            saturation_delta=-10,
        ),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )

    # === BLUE ===
    blue_candidates = [c for c in colors if 190 < c.hsl[0] < 260 and c.hsl[1] > 25]
    if blue_candidates:
        blue_base = sorted(blue_candidates, key=lambda c: c.luminance, reverse=True)[0]
    else:
        blue_base = palette["info"]
    palette["blue"] = ensure_terminal_contrast(
        blue_base, bg, bg_light, MIN_TERMINAL_CONTRAST, is_dark_theme
    )
    palette["blue_bright"] = ensure_terminal_contrast(
        adjust_color(palette["blue"], lightness_delta=15),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )
    palette["blue_dim"] = ensure_terminal_contrast(
        adjust_color(
            palette["blue"],
            lightness_delta=-15 if is_dark_theme else 12,
            saturation_delta=-10,
        ),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )

    # === MAGENTA ===
    magenta_candidates = [
        c for c in colors if (c.hsl[0] > 280 or c.hsl[0] < 20) and c.hsl[1] > 30
    ]
    if magenta_candidates:
        magenta_base = sorted(magenta_candidates, key=lambda c: c.hsl[1], reverse=True)[
            0
        ]
    else:
        magenta_base = create_color(*hsl_to_rgb(300, 50, 55))
    palette["magenta"] = ensure_terminal_contrast(
        magenta_base, bg, bg_light, MIN_TERMINAL_CONTRAST, is_dark_theme
    )
    palette["magenta_bright"] = ensure_terminal_contrast(
        adjust_color(palette["magenta"], lightness_delta=15),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )
    palette["magenta_dim"] = ensure_terminal_contrast(
        adjust_color(
            palette["magenta"],
            lightness_delta=-15 if is_dark_theme else 12,
            saturation_delta=-10,
        ),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )

    # === CYAN ===
    cyan_candidates = [c for c in colors if 160 < c.hsl[0] < 200 and c.hsl[1] > 25]
    if cyan_candidates:
        cyan_base = cyan_candidates[0]
    else:
        cyan_base = create_color(*hsl_to_rgb(180, 50, 50))
    palette["cyan"] = ensure_terminal_contrast(
        cyan_base, bg, bg_light, MIN_TERMINAL_CONTRAST, is_dark_theme
    )
    palette["cyan_bright"] = ensure_terminal_contrast(
        adjust_color(palette["cyan"], lightness_delta=15),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )
    palette["cyan_dim"] = ensure_terminal_contrast(
        adjust_color(
            palette["cyan"],
            lightness_delta=-15 if is_dark_theme else 12,
            saturation_delta=-10,
        ),
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )

    # === WHITE ===
    # White should always be light, desaturated to ensure pure gray tones
    if is_dark_theme:
        white_lightness = fg_dim.hsl[2]
        # Push white to at least 75%, and white_bright to at least 90%
        palette["white"] = create_color(*hsl_to_rgb(0, 0, max(75, white_lightness)))
        palette["white_bright"] = create_color(*hsl_to_rgb(0, 0, max(90, white_lightness + 12)))
        palette["white_dim"] = create_color(*hsl_to_rgb(0, 0, max(60, white_lightness - 8)))
    else:
        white_lightness = bg.hsl[2]
        palette["white"] = create_color(*hsl_to_rgb(0, 0, white_lightness))
        palette["white_bright"] = create_color(*hsl_to_rgb(0, 0, min(97, white_lightness + 3)))
        palette["white_dim"] = create_color(*hsl_to_rgb(0, 0, max(40, white_lightness - 25)))

    # Ensure white_dim meets contrast requirements
    palette["white_dim"] = ensure_terminal_contrast(
        palette["white_dim"],
        bg,
        bg_light,
        MIN_TERMINAL_CONTRAST,
        is_dark_theme,
    )
