"""Image sampler widget for displaying and sampling colors from an image."""

from textual.widgets import Static
from textual.reactive import reactive
from textual.message import Message
from PIL import Image
import numpy as np

from ...types import Color
from ...color import create_color


class ImageSampler(Static):
    """Displays a block-character representation of an image for color sampling."""

    DEFAULT_CSS = ""

    image_path: reactive[str] = reactive("")

    # Cached image data
    _image_array: np.ndarray | None = None
    _original_size: tuple[int, int] = (0, 0)
    _pil_image: Image.Image | None = None

    class ColorSampled(Message):
        """Emitted when a color is sampled from the image."""

        def __init__(self, color: Color, x: int, y: int) -> None:
            self.color = color
            self.x = x
            self.y = y
            super().__init__()

    def __init__(self, image_path: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self.image_path = image_path

    def watch_image_path(self, path: str) -> None:
        """Load image when path changes."""
        if path:
            self._load_image(path)
            self.refresh()

    def _load_image(self, path: str) -> None:
        """Load the original image."""
        try:
            self._pil_image = Image.open(path).convert("RGB")
            self._original_size = self._pil_image.size
        except Exception:
            self._pil_image = None
            self._original_size = (0, 0)
            self._image_array = None

    def _resize_for_display(self) -> None:
        """Resize image to fit current widget size."""
        if self._pil_image is None:
            return

        # Get available size (accounting for border and padding)
        width = self.size.width - 4  # border + padding
        height = (self.size.height - 3) * 2  # header line, border, *2 for half-blocks

        if width <= 0 or height <= 0:
            return

        # Resize maintaining aspect ratio to fill available space
        img_aspect = self._original_size[0] / self._original_size[1]
        display_aspect = width / height

        if img_aspect > display_aspect:
            # Image is wider - fit to width
            display_width = width
            display_height = int(width / img_aspect)
        else:
            # Image is taller - fit to height
            display_height = height
            display_width = int(height * img_aspect)

        display_img = self._pil_image.resize(
            (max(1, display_width), max(1, display_height)),
            Image.Resampling.NEAREST,
        )
        self._image_array = np.array(display_img)

    def on_resize(self, event) -> None:
        """Re-render image when widget resizes."""
        self._resize_for_display()
        self.refresh()

    def render(self) -> str:
        """Render the image using block characters."""
        # Ensure we have the right size for current widget dimensions
        if self._pil_image is not None and self._image_array is None:
            self._resize_for_display()

        if self._image_array is None:
            if self.image_path:
                return f"[dim]Could not load: {self.image_path}[/]"
            return "[dim]No image loaded[/]"

        lines = [f"[bold]{self.image_path.split('/')[-1]}[/] [dim](click to sample)[/]"]

        # Use half-block characters to show 2 vertical pixels per character
        for y in range(0, self._image_array.shape[0] - 1, 2):
            line = ""
            for x in range(self._image_array.shape[1]):
                upper_rgb = self._image_array[y, x]
                lower_rgb = self._image_array[y + 1, x]

                upper_hex = "#{:02x}{:02x}{:02x}".format(*upper_rgb)
                lower_hex = "#{:02x}{:02x}{:02x}".format(*lower_rgb)

                line += f"[{upper_hex} on {lower_hex}]▀[/]"

            lines.append(line)

        return "\n".join(lines)

    def on_click(self, event) -> None:
        """Handle click events to sample colors."""
        if self._image_array is None or self._original_size[0] == 0:
            return

        # Calculate click position relative to image
        # Account for border and header line
        click_x = event.x - 2  # border + padding
        click_y = (event.y - 2) * 2  # header + border, *2 for half-blocks

        if click_x < 0 or click_y < 0:
            return
        if click_x >= self._image_array.shape[1]:
            return
        if click_y >= self._image_array.shape[0]:
            return

        # Get the pixel color
        rgb = self._image_array[click_y, click_x]
        color = create_color(int(rgb[0]), int(rgb[1]), int(rgb[2]))

        # Map to original image coordinates
        display_width = self._image_array.shape[1]
        display_height = self._image_array.shape[0]
        orig_x = int(click_x * self._original_size[0] / display_width)
        orig_y = int(click_y * self._original_size[1] / display_height)

        self.post_message(self.ColorSampled(color, orig_x, orig_y))
