"""Start screen for the TUI application."""

import os
from pathlib import Path

from textual.screen import Screen
from textual.widgets import Static, Button, Input, Label
from textual.containers import Vertical, Horizontal
from textual.message import Message


class StartScreen(Screen):
    """Initial screen for setting up image and output directory."""

    DEFAULT_CSS = """
    StartScreen {
        align: center middle;
    }

    #start-container {
        width: 70;
        height: 30;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    .title {
        text-style: bold;
        text-align: center;
        height: 1;
        margin-bottom: 1;
    }

    .subtitle {
        text-align: center;
        color: $text-muted;
        height: 1;
        margin-bottom: 1;
    }

    .form-row {
        height: 5;
    }

    .form-row Label {
        height: 1;
    }

    .input-row {
        height: 3;
    }

    .input-row Input {
        width: 1fr;
    }

    .input-row Button {
        width: 12;
        margin: 0 0 0 1;
    }

    #preview {
        height: 1;
        margin: 1 0;
    }

    .action-buttons {
        height: 5;
        margin-top: 1;
        align: center middle;
    }

    .action-buttons Button {
        margin: 0 1;
        min-width: 16;
    }
    """

    class StartRequested(Message):
        """Emitted when user wants to start editing."""

        def __init__(self, image_path: str, output_dir: str, theme_name: str) -> None:
            self.image_path = image_path
            self.output_dir = output_dir
            self.theme_name = theme_name
            super().__init__()

    def __init__(
        self,
        initial_image: str = "",
        initial_output: str = "",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.initial_image = initial_image
        self.initial_output = initial_output or os.getcwd()

    def compose(self):
        with Vertical(id="start-container"):
            yield Static("[bold]Color Palette Generator[/]", classes="title")
            yield Static(
                "Generate color palettes from images",
                classes="subtitle",
            )

            with Vertical(classes="form-row"):
                yield Label("Image file:")
                with Horizontal(classes="input-row"):
                    yield Input(
                        value=self.initial_image,
                        placeholder="Path to image file...",
                        id="image-input",
                    )
                    yield Button("Browse", id="browse-image-btn")

            with Vertical(classes="form-row"):
                yield Label("Output directory:")
                with Horizontal(classes="input-row"):
                    yield Input(
                        value=self.initial_output,
                        placeholder="Output directory...",
                        id="output-input",
                    )
                    yield Button("Browse", id="browse-output-btn")

            with Vertical(classes="form-row"):
                yield Label("Theme name (optional):")
                yield Input(
                    placeholder="Derived from image name if empty",
                    id="name-input",
                )

            yield Static("[dim]Select an image to preview[/]", id="preview")

            with Horizontal(classes="action-buttons"):
                yield Button(
                    "Start Editing",
                    id="start-btn",
                    variant="primary",
                    disabled=True,
                )
                yield Button("Quit", id="quit-btn")

    def on_mount(self) -> None:
        """Check initial state."""
        self._validate_inputs()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        self._validate_inputs()

        # Update preview when image path changes
        if event.input.id == "image-input":
            self._update_preview(event.value)

    def _validate_inputs(self) -> None:
        """Validate inputs and enable/disable start button."""
        image_input = self.query_one("#image-input", Input)
        image_path = image_input.value.strip()

        start_btn = self.query_one("#start-btn", Button)

        # Check if image exists and is a file
        if image_path and os.path.isfile(image_path):
            # Check if it's an image
            ext = Path(image_path).suffix.lower()
            image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
            start_btn.disabled = ext not in image_extensions
        else:
            start_btn.disabled = True

    def _update_preview(self, path: str) -> None:
        """Update the preview area."""
        preview = self.query_one("#preview", Static)

        if not path:
            preview.update("[dim]Select an image to preview[/]")
            return

        path = path.strip()
        if not os.path.isfile(path):
            preview.update(f"[red]File not found:[/] {path}")
            return

        ext = Path(path).suffix.lower()
        image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
        if ext not in image_extensions:
            preview.update(f"[red]Not an image file:[/] {path}")
            return

        # Show file info
        size = os.path.getsize(path)
        size_str = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f} MB"
        name = os.path.basename(path)
        preview.update(f"[green]Ready:[/] {name} ({size_str})")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "quit-btn":
            self.app.exit()

        elif event.button.id == "browse-image-btn":
            from .file_browser import ImageBrowserScreen

            def handle_result(result):
                if result:
                    image_input = self.query_one("#image-input", Input)
                    image_input.value = result.path
                    self._validate_inputs()
                    self._update_preview(result.path)

            self.app.push_screen(
                ImageBrowserScreen(start_path=os.getcwd()),
                handle_result,
            )

        elif event.button.id == "browse-output-btn":
            from .file_browser import DirectoryPickerScreen

            output_input = self.query_one("#output-input", Input)

            def handle_result(result):
                if result:
                    output_input.value = result.path

            self.app.push_screen(
                DirectoryPickerScreen(
                    start_path=os.getcwd(),
                    current_value=output_input.value,
                ),
                handle_result,
            )

        elif event.button.id == "start-btn":
            image_path = self.query_one("#image-input", Input).value.strip()
            output_dir = self.query_one("#output-input", Input).value.strip()
            theme_name = self.query_one("#name-input", Input).value.strip()

            if not theme_name:
                theme_name = Path(image_path).stem

            if not output_dir:
                output_dir = os.path.dirname(image_path) or os.getcwd()

            self.dismiss(
                self.StartRequested(
                    image_path=image_path,
                    output_dir=output_dir,
                    theme_name=theme_name,
                )
            )
