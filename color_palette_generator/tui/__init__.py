"""TUI module for interactive color palette generation."""

from .app import PaletteApp


def run_tui(
    image_path: str = "",
    output_dir: str = "",
    theme_name: str = "",
) -> None:
    """Launch the TUI application.

    Args:
        image_path: Optional path to the source image (shows file picker if empty)
        output_dir: Optional output directory (defaults to cwd)
        theme_name: Optional theme name (defaults to image filename)
    """
    app = PaletteApp(
        image_path=image_path,
        output_dir=output_dir,
        theme_name=theme_name,
    )
    app.run()


__all__ = ["run_tui", "PaletteApp"]
