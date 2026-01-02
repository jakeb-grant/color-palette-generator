"""Export screen modal for format selection."""

from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, RadioButton, RadioSet
from textual.containers import Vertical, Horizontal
from textual.message import Message


class ExportScreen(ModalScreen):
    """Modal dialog for export options."""

    DEFAULT_CSS = """
    ExportScreen {
        align: center middle;
    }

    #export-dialog {
        width: 60;
        height: auto;
        max-height: 80%;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #export-dialog Label {
        margin: 0;
    }

    #export-dialog Input {
        margin: 0 0 1 0;
    }

    #export-dialog RadioSet {
        margin: 0;
        height: auto;
    }

    #export-dialog .buttons {
        margin-top: 1;
        height: 3;
    }

    #export-dialog .buttons Button {
        margin: 0 1;
    }
    """

    class ExportRequested(Message):
        """Emitted when export is confirmed."""

        def __init__(
            self,
            theme_name: str,
            output_dir: str,
            export_format: str,
        ) -> None:
            self.theme_name = theme_name
            self.output_dir = output_dir
            self.export_format = export_format
            super().__init__()

    def __init__(
        self,
        default_name: str = "",
        default_dir: str = "",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.default_name = default_name
        self.default_dir = default_dir

    def compose(self):
        with Vertical(id="export-dialog"):
            yield Label("[bold]Export Palette[/]")

            yield Label("Theme name:")
            yield Input(
                value=self.default_name,
                placeholder="my-theme",
                id="theme-name",
            )

            yield Label("Output directory:")
            yield Input(
                value=self.default_dir,
                placeholder="./out",
                id="output-dir",
            )

            yield Label("Export format:")
            with RadioSet(id="format-select"):
                yield RadioButton("Palette JSON only", value=True, id="format-json")
                yield RadioButton("Zed themes", id="format-zed")
                yield RadioButton("HTML preview", id="format-html")
                yield RadioButton("All formats", id="format-all")

            with Horizontal(classes="buttons"):
                yield Button("Export", id="export-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "export-btn":
            # Get values
            theme_name = self.query_one("#theme-name", Input).value
            output_dir = self.query_one("#output-dir", Input).value
            radio_set = self.query_one("#format-select", RadioSet)

            # Determine format from selected radio
            format_map = {
                "format-json": "json",
                "format-zed": "zed",
                "format-html": "html",
                "format-all": "all",
            }
            export_format = "json"
            if radio_set.pressed_button:
                export_format = format_map.get(
                    radio_set.pressed_button.id, "json"
                )

            self.dismiss(
                self.ExportRequested(
                    theme_name=theme_name or self.default_name,
                    output_dir=output_dir or self.default_dir,
                    export_format=export_format,
                )
            )
