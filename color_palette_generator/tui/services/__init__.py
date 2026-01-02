"""TUI services for color extraction and palette generation."""

from .pixel_sampler import snap_to_real_colors, sample_pixel_at_position
from .palette_bridge import generate_palette_from_selections

__all__ = [
    "snap_to_real_colors",
    "sample_pixel_at_position",
    "generate_palette_from_selections",
]
