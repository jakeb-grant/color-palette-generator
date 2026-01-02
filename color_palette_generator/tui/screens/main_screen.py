"""Main screen layout for the TUI."""

from textual.screen import Screen

from ..widgets import (
    ImageSampler,
    ColorListView,
    RolePanel,
    ContrastReport,
    ActionBar,
)


class MainScreen(Screen):
    """Primary interface for palette editing."""

    DEFAULT_CSS = """
    MainScreen {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 1fr 1fr;
        grid-rows: 1fr 1fr;
    }

    #left-top {
        column-span: 1;
        row-span: 1;
    }

    #right-top {
        column-span: 1;
        row-span: 1;
    }

    #left-bottom {
        column-span: 1;
        row-span: 1;
    }

    #right-bottom {
        column-span: 1;
        row-span: 1;
    }
    """

    def compose(self):
        # Top row: Image sampler and Color list
        yield ImageSampler(id="image-sampler")
        yield ColorListView(id="color-list", title="Extracted Colors")

        # Bottom row: Contrast report and Role panel
        yield ContrastReport(id="contrast-report")
        yield RolePanel(id="role-panel")

        # Action bar at bottom
        yield ActionBar(id="action-bar")
