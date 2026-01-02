"""File browser screen for selecting images and directories."""

import os

from textual.screen import Screen
from textual.widgets import DirectoryTree, Static, Button, Input, Label
from textual.containers import Vertical, Horizontal
from textual.message import Message


class FilteredDirectoryTree(DirectoryTree):
    """Directory tree that filters for image files."""

    def filter_paths(self, paths):
        """Filter to show directories and image files only."""
        image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
        filtered = []
        for path in paths:
            if path.is_dir():
                filtered.append(path)
            elif path.suffix.lower() in image_extensions:
                filtered.append(path)
        return sorted(filtered, key=lambda p: (not p.is_dir(), p.name.lower()))


class ImageBrowserScreen(Screen):
    """Screen for browsing and selecting an image file."""

    DEFAULT_CSS = """
    ImageBrowserScreen {
        align: center middle;
    }

    #browser-container {
        width: 80%;
        height: 80%;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #browser-container .title {
        text-style: bold;
        margin-bottom: 1;
    }

    #path-display {
        margin: 1 0;
        padding: 0 1;
        background: $background;
    }

    #tree-container {
        height: 1fr;
        margin: 1 0;
        border: solid $secondary;
    }

    FilteredDirectoryTree {
        height: 100%;
    }

    #selected-display {
        margin: 1 0;
        padding: 0 1;
        height: 1;
    }

    .buttons {
        height: 3;
        margin-top: 1;
    }

    .buttons Button {
        margin: 0 1;
    }
    """

    class ImageSelected(Message):
        """Emitted when an image is selected."""

        def __init__(self, path: str) -> None:
            self.path = path
            super().__init__()

    def __init__(self, start_path: str = ".", **kwargs) -> None:
        super().__init__(**kwargs)
        self.start_path = os.path.abspath(start_path)
        self.selected_path: str | None = None

    def compose(self):
        with Vertical(id="browser-container"):
            yield Static("[bold]Select Image[/]", classes="title")
            yield Static(f"[dim]{self.start_path}[/]", id="path-display")

            with Vertical(id="tree-container"):
                yield FilteredDirectoryTree(self.start_path, id="file-tree")

            yield Static("[dim]No file selected[/]", id="selected-display")

            with Horizontal(classes="buttons"):
                yield Button("Select", id="select-btn", variant="primary", disabled=True)
                yield Button("Cancel", id="cancel-btn")

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection."""
        self.selected_path = str(event.path)
        display = self.query_one("#selected-display", Static)
        display.update(f"[green]Selected:[/] {event.path.name}")

        select_btn = self.query_one("#select-btn", Button)
        select_btn.disabled = False

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        """Handle directory navigation."""
        path_display = self.query_one("#path-display", Static)
        path_display.update(f"[dim]{event.path}[/]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "select-btn" and self.selected_path:
            self.dismiss(self.ImageSelected(self.selected_path))


class DirectoryPickerScreen(Screen):
    """Screen for selecting an output directory."""

    DEFAULT_CSS = """
    DirectoryPickerScreen {
        align: center middle;
    }

    #picker-container {
        width: 80%;
        height: 80%;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #picker-container .title {
        text-style: bold;
        margin-bottom: 1;
    }

    #dir-input {
        margin: 1 0;
    }

    #tree-container {
        height: 1fr;
        margin: 1 0;
        border: solid $secondary;
    }

    DirectoryTree {
        height: 100%;
    }

    #current-dir {
        margin: 1 0;
        padding: 0 1;
        height: 1;
    }

    .buttons {
        height: 3;
        margin-top: 1;
    }

    .buttons Button {
        margin: 0 1;
    }
    """

    class DirectorySelected(Message):
        """Emitted when a directory is selected."""

        def __init__(self, path: str) -> None:
            self.path = path
            super().__init__()

    def __init__(self, start_path: str = ".", current_value: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self.start_path = os.path.abspath(start_path)
        self.current_value = current_value or self.start_path
        self.selected_dir = self.current_value

    def compose(self):
        with Vertical(id="picker-container"):
            yield Static("[bold]Select Output Directory[/]", classes="title")

            yield Label("Path:")
            yield Input(value=self.current_value, id="dir-input")

            with Vertical(id="tree-container"):
                yield DirectoryTree(self.start_path, id="dir-tree")

            yield Static(f"[dim]{self.selected_dir}[/]", id="current-dir")

            with Horizontal(classes="buttons"):
                yield Button("Select", id="select-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn")

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        """Handle directory selection in tree."""
        self.selected_dir = str(event.path)
        dir_input = self.query_one("#dir-input", Input)
        dir_input.value = self.selected_dir

        current_display = self.query_one("#current-dir", Static)
        current_display.update(f"[green]{self.selected_dir}[/]")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle manual path input."""
        if event.input.id == "dir-input":
            self.selected_dir = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "select-btn":
            self.dismiss(self.DirectorySelected(self.selected_dir))
