from ..image import extract_colors, find_average_color
from .backgrounds import generate_background_colors, ensure_background_contrast
from .foregrounds import generate_foreground_colors
from .accents import generate_accent_colors
from .semantic import generate_semantic_colors
from .terminal import generate_terminal_colors


def generate_functional_palette(image_path, force_theme=None):
    """Generate a functional color palette with strict readability.

    Args:
        image_path: Path to the source image
        force_theme: "dark", "light", or None (auto-detect from image)

    Returns:
        tuple: (palette dict, extracted colors list, average color, is_dark_theme bool)
    """
    colors = extract_colors(image_path, n_colors=20)
    avg_color = find_average_color(image_path)

    # Determine if this should be a dark or light theme
    if force_theme is not None:
        is_dark_theme = force_theme == "dark"
    else:
        is_dark_theme = avg_color.luminance < 0.5

    # Generate palette in order (each step may depend on previous)
    palette = generate_background_colors(colors, is_dark_theme)
    ensure_background_contrast(palette, is_dark_theme)

    generate_foreground_colors(colors, palette, is_dark_theme)
    generate_accent_colors(colors, palette, is_dark_theme)
    generate_semantic_colors(palette, is_dark_theme)
    generate_terminal_colors(colors, palette, is_dark_theme)

    return palette, colors, avg_color, is_dark_theme
