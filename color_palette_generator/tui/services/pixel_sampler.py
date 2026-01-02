"""Pixel sampling services for snap-to-real-color functionality."""

import numpy as np
from PIL import Image

from ...types import Color
from ...color import create_color


def snap_to_real_colors(
    image_path: str,
    centroid_colors: list[Color],
) -> list[Color]:
    """Find the closest actual pixel in the image for each centroid.

    This addresses the fundamental issue with k-means clustering where
    cluster centroids may not represent actual colors in the image.

    Args:
        image_path: Path to source image
        centroid_colors: List of k-means centroid colors

    Returns:
        List of real pixel colors, one for each centroid
    """
    img = Image.open(image_path).convert("RGB")

    # Resize for faster processing (same as extraction)
    max_size = 300
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.Resampling.NEAREST)

    pixels = np.array(img).reshape(-1, 3)

    real_colors = []
    for centroid in centroid_colors:
        # Find pixel with minimum Euclidean distance to centroid
        centroid_rgb = np.array(centroid.rgb)
        distances = np.linalg.norm(pixels - centroid_rgb, axis=1)
        closest_idx = np.argmin(distances)
        closest_pixel = pixels[closest_idx]

        real_colors.append(
            create_color(
                int(closest_pixel[0]),
                int(closest_pixel[1]),
                int(closest_pixel[2]),
            )
        )

    return real_colors


def sample_pixel_at_position(
    image_path: str,
    x: int,
    y: int,
) -> Color:
    """Sample a specific pixel from the image.

    Args:
        image_path: Path to source image
        x: X coordinate in original image
        y: Y coordinate in original image

    Returns:
        Color at the specified position
    """
    img = Image.open(image_path).convert("RGB")

    # Clamp coordinates to valid range
    x = max(0, min(x, img.size[0] - 1))
    y = max(0, min(y, img.size[1] - 1))

    r, g, b = img.getpixel((x, y))
    return create_color(r, g, b)


def get_color_histogram(
    image_path: str,
    n_colors: int = 20,
    ignore_extremes: bool = True,
) -> list[Color]:
    """Extract colors using histogram peaks instead of k-means.

    This is an alternative to k-means that finds actual prevalent
    colors in the image.

    Args:
        image_path: Path to source image
        n_colors: Number of colors to extract
        ignore_extremes: Whether to filter near-black and near-white pixels

    Returns:
        List of prevalent colors from the image
    """
    img = Image.open(image_path).convert("RGB")

    # Resize for faster processing
    max_size = 300
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.Resampling.NEAREST)

    # Quantize to reduce color space
    quantized = img.quantize(colors=n_colors * 2, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()

    # Extract colors from palette
    colors = []
    for i in range(0, len(palette), 3):
        if i // 3 >= n_colors:
            break

        r, g, b = palette[i], palette[i + 1], palette[i + 2]

        if ignore_extremes:
            # Skip near-black and near-white
            total = r + g + b
            if total < 30 or total > 735:
                continue

        colors.append(create_color(r, g, b))

    return colors[:n_colors]
