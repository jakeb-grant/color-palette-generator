"""Main TUI application for interactive palette generation."""

import os
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.widgets import Footer, Header

from ..types import Color
from ..image.extraction import extract_colors
from ..palette import generate_functional_palette
from ..export import export_json, create_html_preview
from ..zed import generate_zed_theme
from ..opacity import calculate_theme_opacity
from ..color.manipulation import adjust_color, create_color
from ..color.conversion import hsl_to_rgb
from ..color.contrast import ensure_terminal_contrast

from .state import AppState, ANSI_FAMILIES, DERIVABLE_GROUPS, ROLE_CONTRAST_REQUIREMENTS
from .widgets import (
    ImageSampler,
    ColorListView,
    RolePanel,
    ContrastReport,
)
from .screens import ExportScreen, StartScreen, HelpScreen
from .services import snap_to_real_colors


class PaletteApp(App):
    """Interactive color palette generator TUI."""

    TITLE = "Color Palette Generator"

    CSS = """
    #main-grid {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 1fr 1fr;
        grid-rows: 1fr 1fr;
        height: 100%;
    }

    #image-panel {
        column-span: 1;
        row-span: 1;
    }

    #color-list-panel {
        column-span: 1;
        row-span: 1;
    }

    #contrast-panel {
        column-span: 1;
        row-span: 1;
    }

    #role-panel {
        column-span: 1;
        row-span: 1;
    }

    ImageSampler {
        height: 100%;
    }

    ColorListView {
        height: 100%;
    }

    ContrastReport {
        height: 100%;
    }

    RolePanel {
        height: 100%;
    }
    """

    BINDINGS = [
        # Primary actions (shown in footer)
        Binding("question_mark", "show_help", "Help", key_display="?"),
        Binding("q", "quit", "Quit"),
        Binding("g", "generate", "Generate"),
        Binding("s", "snap", "Snap"),
        Binding("e", "export", "Export"),
        Binding("t", "toggle_theme", "Theme"),
        Binding("n", "new_image", "New"),
        Binding("d", "derive_family", "Derive"),
        Binding("f", "fix_contrast", "Fix"),
        Binding("r", "restore_role", "Restore"),
        # Hidden from footer (still work, shown in help)
        Binding("enter", "assign", "Assign Color", show=False),
        Binding("escape", "clear_selection", "Clear Selection", show=False),
        # Opacity adjustment (hidden, documented in help)
        Binding("o", "opacity_down", "Opacity -", show=False),
        Binding("O", "opacity_up", "Opacity +", show=False),
        # HSL adjustment (hidden, documented in help)
        Binding("h", "hue_down", "Hue -", show=False),
        Binding("H", "hue_up", "Hue +", show=False),
        Binding("[", "sat_down", "Sat -", show=False),
        Binding("]", "sat_up", "Sat +", show=False),
        Binding("l", "light_down", "Light -", show=False),
        Binding("L", "light_up", "Light +", show=False),
    ]

    def __init__(
        self,
        image_path: str = "",
        output_dir: str = "",
        theme_name: str = "",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.state = AppState()
        self._initial_image = image_path
        self._initial_output = output_dir or os.getcwd()
        self._initial_theme = theme_name
        self._selected_color: Color | None = None
        self._selected_color_index: int | None = None
        self._is_initialized = False
        self._original_palette: dict[str, Color] = {}  # Store original generated palette

    def compose(self) -> ComposeResult:
        yield Header()
        with Grid(id="main-grid"):
            yield ImageSampler(id="image-panel")
            yield ColorListView(title="Extracted Colors", id="color-list-panel")
            yield ContrastReport(id="contrast-panel")
            yield RolePanel(id="role-panel")
        yield Footer()

    def on_mount(self) -> None:
        """Show start screen or load image on mount."""
        if self._initial_image and os.path.isfile(self._initial_image):
            # Direct mode - load the provided image
            self._load_image(
                self._initial_image,
                self._initial_output,
                self._initial_theme or Path(self._initial_image).stem,
            )
        else:
            # Show start screen to select image
            self._show_start_screen()

    def _show_start_screen(self) -> None:
        """Show the start screen for image/output selection."""
        def handle_start(result):
            if result:
                self._load_image(
                    result.image_path,
                    result.output_dir,
                    result.theme_name,
                )

        self.push_screen(
            StartScreen(
                initial_image=self._initial_image,
                initial_output=self._initial_output,
            ),
            handle_start,
        )

    def _load_image(self, image_path: str, output_dir: str, theme_name: str) -> None:
        """Load an image and initialize the palette editor."""
        self.state.image_path = image_path
        self.state.output_dir = output_dir
        self.state.theme_name = theme_name

        # Reset state for new image
        self.state.extracted_colors = []
        self.state.real_pixel_colors = []
        self.state.sampled_colors = []
        self.state.role_assignments = {}
        self.state.palette = {}
        self._selected_color = None
        self._selected_color_index = None

        # Update image sampler
        image_sampler = self.query_one("#image-panel", ImageSampler)
        image_sampler.image_path = image_path

        # Load colors
        self._load_colors()
        self._is_initialized = True

    def _load_colors(self) -> None:
        """Load colors from image."""
        if not self.state.image_path:
            return

        # Extract colors using k-means (100 colors for more variety)
        self.state.extracted_colors = extract_colors(self.state.image_path, n_colors=100)

        # Compute snap-to-real colors
        self.state.real_pixel_colors = snap_to_real_colors(
            self.state.image_path,
            self.state.extracted_colors,
        )

        # Default to using real pixel colors
        self.state.use_real_colors = True

        # Update color list widget
        self._update_color_list()

        # Auto-generate initial palette
        self._generate_palette()

    def _update_color_list(self) -> None:
        """Update the color list widget with current colors."""
        color_list = self.query_one("#color-list-panel", ColorListView)
        color_list.colors = self.state.active_colors

    def _generate_palette(self) -> None:
        """Generate palette from current state."""
        if not self.state.image_path:
            return

        # Use existing generate function
        palette, colors, avg_color, is_dark = generate_functional_palette(
            self.state.image_path,
            force_theme="dark" if self.state.is_dark_theme else "light",
        )

        # Store original before applying user overrides
        self._original_palette = palette.copy()

        # Apply any user role assignments
        for role, color in self.state.role_assignments.items():
            palette[role] = color

        self.state.palette = palette

        # Update widgets
        self._update_palette_widgets()
        self.notify("Palette generated")

    def _update_palette_widgets(self) -> None:
        """Update all palette-related widgets."""
        palette = self.state.palette

        # Update contrast report
        contrast_report = self.query_one("#contrast-panel", ContrastReport)
        contrast_report.palette = palette
        contrast_report.is_dark_theme = self.state.is_dark_theme

        # Update role panel with assignments
        role_panel = self.query_one("#role-panel", RolePanel)
        role_panel.role_assignments = palette.copy()

        # Update contrast ratios in role panel
        ratios = contrast_report.get_contrast_ratios()
        role_panel.contrast_ratios = ratios

    # --- Message Handlers ---

    def on_color_list_view_color_selected(
        self, event: ColorListView.ColorSelected
    ) -> None:
        """Handle color selection from list."""
        self._selected_color = event.color
        self._selected_color_index = event.index
        self.state.selected_color_index = event.index
        self.notify(f"Selected: {event.color.hex}")

    def on_role_panel_role_selected(self, event: RolePanel.RoleSelected) -> None:
        """Handle role selection."""
        self.state.selected_role = event.role_name

        # If a color is selected, assign it
        if self._selected_color:
            self._assign_color_to_role(event.role_name, self._selected_color)

    def on_image_sampler_color_sampled(
        self, event: ImageSampler.ColorSampled
    ) -> None:
        """Handle color sampled from image."""
        color = event.color
        self.state.sampled_colors.append(color)

        # Add to color list
        self.state.extracted_colors.append(color)
        self._update_color_list()

        # Select the newly sampled color
        color_list = self.query_one("#color-list-panel", ColorListView)
        new_index = len(self.state.extracted_colors) - 1
        color_list.select_by_index(new_index)
        self._selected_color = color
        self._selected_color_index = new_index

        self.notify(f"Sampled: {color.hex} at ({event.x}, {event.y})")

    # --- Actions ---

    def action_show_help(self) -> None:
        """Show help screen."""
        self.push_screen(HelpScreen())

    def action_generate(self) -> None:
        """Generate palette action."""
        if self._is_initialized:
            self._generate_palette()

    def action_snap(self) -> None:
        """Toggle snap-to-real action."""
        if not self._is_initialized:
            return
        self.state.use_real_colors = not self.state.use_real_colors
        self._update_color_list()
        mode = "real pixels" if self.state.use_real_colors else "k-means centroids"
        self.notify(f"Using {mode}")

    def action_export(self) -> None:
        """Show export dialog."""
        if not self._is_initialized:
            return

        def handle_export_result(result):
            if result:
                self._do_export(result)

        self.push_screen(
            ExportScreen(
                default_name=self.state.theme_name,
                default_dir=self.state.output_dir,
            ),
            handle_export_result,
        )

    def action_toggle_theme(self) -> None:
        """Toggle between dark and light theme mode."""
        if not self._is_initialized:
            return
        self.state.is_dark_theme = not self.state.is_dark_theme
        self._generate_palette()
        mode = "dark" if self.state.is_dark_theme else "light"
        self.notify(f"Switched to {mode} mode")

    def action_new_image(self) -> None:
        """Select a new image."""
        self._show_start_screen()

    def action_assign(self) -> None:
        """Assign selected color to selected role."""
        if self._selected_color and self.state.selected_role:
            self._assign_color_to_role(
                self.state.selected_role, self._selected_color
            )

    def action_clear_selection(self) -> None:
        """Clear current selection."""
        self._selected_color = None
        self._selected_color_index = None
        self.state.selected_color_index = None
        self.state.selected_role = None

        # Clear visual selection in role panel
        try:
            role_panel = self.query_one("#role-panel", RolePanel)
            role_panel.selected_role = None
        except Exception:
            pass

        self.notify("Selection cleared")

    def action_restore_role(self) -> None:
        """Restore selected role to its original generated color."""
        if not self._is_initialized:
            return

        role = self.state.selected_role
        if not role:
            self.notify("Select a role first")
            return

        if role not in self._original_palette:
            self.notify(f"No original color for {role}")
            return

        original_color = self._original_palette[role]

        # Remove from user overrides
        if role in self.state.role_assignments:
            del self.state.role_assignments[role]

        # Restore original
        self.state.palette[role] = original_color

        self._update_palette_widgets()
        self.notify(f"Restored {role} to {original_color.hex}")

    def action_opacity_down(self) -> None:
        """Decrease blur opacity by 5%."""
        if not self._is_initialized:
            return
        current = self.state.blur_opacity
        if current is None:
            # Start from auto-calculated value
            current = calculate_theme_opacity(self.state.palette, self.state.is_dark_theme)
        new_opacity = max(0.0, current - 0.05)
        self.state.blur_opacity = new_opacity
        self.notify(f"Opacity: {new_opacity:.0%}")

    def action_opacity_up(self) -> None:
        """Increase blur opacity by 5%."""
        if not self._is_initialized:
            return
        current = self.state.blur_opacity
        if current is None:
            # Start from auto-calculated value
            current = calculate_theme_opacity(self.state.palette, self.state.is_dark_theme)
        new_opacity = min(1.0, current + 0.05)
        self.state.blur_opacity = new_opacity
        self.notify(f"Opacity: {new_opacity:.0%}")

    def action_fix_contrast(self) -> None:
        """Auto-fix contrast for all terminal colors against background."""
        if not self._is_initialized:
            return

        bg = self.state.palette.get("background")
        bg_light = self.state.palette.get("background_light", bg)

        if not bg:
            self.notify("No background color set")
            return

        fixed_count = 0
        is_dark = self.state.is_dark_theme

        # Fix all roles that have contrast requirements
        for role, required_contrast in ROLE_CONTRAST_REQUIREMENTS.items():
            if role not in self.state.palette:
                continue

            color = self.state.palette[role]
            fixed_color = ensure_terminal_contrast(
                color, bg, bg_light, required_contrast, is_dark
            )

            # Check if color was actually changed
            if fixed_color.hex != color.hex:
                self.state.palette[role] = fixed_color
                self.state.role_assignments[role] = fixed_color
                fixed_count += 1

        self._update_palette_widgets()

        if fixed_count > 0:
            self.notify(f"Fixed contrast for {fixed_count} colors")
        else:
            self.notify("All colors already meet contrast requirements")

    def action_derive_family(self) -> None:
        """Derive variants from selected color for a role family."""
        if not self._is_initialized:
            return

        if not self._selected_color:
            self.notify("Select a color first")
            return

        role = self.state.selected_role
        if not role:
            self.notify("Select a role to derive (e.g., background, red)")
            return

        # Check if it's an ANSI family (base or variant)
        for family in ANSI_FAMILIES:
            if role == family or role.startswith(f"{family}_"):
                self._derive_ansi_family(self._selected_color, family)
                return

        # Check if it's a derivable group (background, element, foreground, border)
        for group_base, roles in DERIVABLE_GROUPS.items():
            if role in roles:
                self._derive_role_group(self._selected_color, group_base)
                return

        self.notify(f"{role} is not a derivable family")

    def action_hue_down(self) -> None:
        """Decrease hue of selected role color."""
        self._adjust_selected_role_color(hue_delta=-10)

    def action_hue_up(self) -> None:
        """Increase hue of selected role color."""
        self._adjust_selected_role_color(hue_delta=10)

    def action_sat_down(self) -> None:
        """Decrease saturation of selected role color."""
        self._adjust_selected_role_color(sat_delta=-5)

    def action_sat_up(self) -> None:
        """Increase saturation of selected role color."""
        self._adjust_selected_role_color(sat_delta=5)

    def action_light_down(self) -> None:
        """Decrease lightness of selected role color."""
        self._adjust_selected_role_color(light_delta=-5)

    def action_light_up(self) -> None:
        """Increase lightness of selected role color."""
        self._adjust_selected_role_color(light_delta=5)

    # --- Helper Methods ---

    def _assign_color_to_role(self, role: str, color: Color) -> None:
        """Assign a color to a palette role."""
        self.state.role_assignments[role] = color
        self.state.palette[role] = color

        # Update widgets
        self._update_palette_widgets()
        self.notify(f"Assigned {color.hex} to {role}")

    def _derive_ansi_family(self, base_color: Color, family: str) -> None:
        """Derive bright/dim variants from a base color for an ANSI family."""
        # Create bright variant (increase lightness)
        bright = adjust_color(base_color, lightness_delta=15)
        # Create dim variant (decrease lightness and saturation)
        dim = adjust_color(base_color, lightness_delta=-15, saturation_delta=-10)

        # Ensure contrast against backgrounds
        bg = self.state.palette.get("background")
        bg_light = self.state.palette.get("background_light", bg)

        if bg and bg_light:
            # Base needs 4.5:1 contrast
            base_adjusted = ensure_terminal_contrast(
                base_color, bg, bg_light, 4.5, self.state.is_dark_theme
            )
            # Bright needs 4.5:1 contrast
            bright = ensure_terminal_contrast(
                bright, bg, bg_light, 4.5, self.state.is_dark_theme
            )
            # Dim only needs 3.0:1 contrast
            dim = ensure_terminal_contrast(
                dim, bg, bg_light, 3.0, self.state.is_dark_theme
            )
        else:
            base_adjusted = base_color

        # Assign all three variants
        self.state.palette[family] = base_adjusted
        self.state.palette[f"{family}_bright"] = bright
        self.state.palette[f"{family}_dim"] = dim

        self.state.role_assignments[family] = base_adjusted
        self.state.role_assignments[f"{family}_bright"] = bright
        self.state.role_assignments[f"{family}_dim"] = dim

        self._update_palette_widgets()
        self.notify(f"Derived {family} family from {base_color.hex}")

    def _derive_role_group(self, base_color: Color, group: str) -> None:
        """Derive all roles in a group from a base color."""
        is_dark = self.state.is_dark_theme

        if group == "background":
            # For backgrounds: base, then progressively lighter
            self.state.palette["background"] = base_color
            self.state.palette["background_medium"] = adjust_color(
                base_color, lightness_delta=10 if is_dark else -10
            )
            self.state.palette["background_light"] = adjust_color(
                base_color, lightness_delta=18 if is_dark else -18
            )
            self.state.palette["background_disabled"] = adjust_color(
                base_color, lightness_delta=-3 if is_dark else 3, saturation_delta=-5
            )

        elif group == "element":
            # For elements: base, hover/active lighter, disabled muted
            self.state.palette["element"] = base_color
            self.state.palette["element_hover"] = adjust_color(
                base_color, lightness_delta=12 if is_dark else -12
            )
            self.state.palette["element_active"] = adjust_color(
                base_color, lightness_delta=15 if is_dark else -15
            )
            self.state.palette["element_selected"] = adjust_color(
                base_color, lightness_delta=15 if is_dark else -15
            )
            self.state.palette["element_disabled"] = adjust_color(
                base_color, lightness_delta=-8 if is_dark else 8, saturation_delta=-15
            )

        elif group == "foreground":
            # For foregrounds: bright to dim progression
            bg = self.state.palette.get("background")
            # Start from base, create variants
            self.state.palette["foreground"] = base_color
            self.state.palette["foreground_bright"] = adjust_color(
                base_color, lightness_delta=5 if is_dark else -5
            )
            self.state.palette["foreground_medium"] = adjust_color(
                base_color, lightness_delta=-5 if is_dark else 5
            )
            self.state.palette["foreground_dim"] = adjust_color(
                base_color, lightness_delta=-12 if is_dark else 12
            )

        elif group == "border":
            # For borders: base, variant slightly different, focused brighter
            self.state.palette["border"] = base_color
            self.state.palette["border_variant"] = adjust_color(
                base_color, lightness_delta=10 if is_dark else -10
            )
            self.state.palette["border_focused"] = adjust_color(
                base_color, lightness_delta=15 if is_dark else -15, saturation_delta=10
            )
            self.state.palette["border_selected"] = adjust_color(
                base_color, lightness_delta=8 if is_dark else -8
            )
            self.state.palette["border_disabled"] = adjust_color(
                base_color, lightness_delta=-15 if is_dark else 15, saturation_delta=-20
            )

        # Update role assignments to track user changes
        for role in DERIVABLE_GROUPS[group]:
            if role in self.state.palette:
                self.state.role_assignments[role] = self.state.palette[role]

        self._update_palette_widgets()
        self.notify(f"Derived {group} group from {base_color.hex}")

    def _adjust_selected_role_color(
        self, hue_delta: int = 0, sat_delta: int = 0, light_delta: int = 0
    ) -> None:
        """Adjust the color of the currently selected role."""
        if not self._is_initialized:
            return

        role = self.state.selected_role
        if not role:
            self.notify("Select a role first")
            return

        if role not in self.state.palette:
            self.notify(f"{role} has no color assigned")
            return

        color = self.state.palette[role]
        h, s, l = color.hsl

        # Apply deltas with clamping
        new_h = (h + hue_delta) % 360
        new_s = max(0, min(100, s + sat_delta))
        new_l = max(0, min(100, l + light_delta))

        # Create new color from adjusted HSL
        r, g, b = hsl_to_rgb(new_h, new_s, new_l)
        new_color = create_color(r, g, b)

        # Update palette
        self.state.palette[role] = new_color
        self.state.role_assignments[role] = new_color

        # If this is a base ANSI color, also update the family variants
        if role in ANSI_FAMILIES:
            self._derive_ansi_family(new_color, role)
        else:
            self._update_palette_widgets()
            self.notify(f"{role}: H{new_h:.0f} S{new_s:.0f} L{new_l:.0f}")

    def _do_export(self, export_request) -> None:
        """Perform the actual export."""
        theme_name = export_request.theme_name
        output_dir = export_request.output_dir
        export_format = export_request.export_format

        os.makedirs(output_dir, exist_ok=True)

        # Update state with new output dir
        self.state.output_dir = output_dir

        palette = self.state.palette
        is_dark = self.state.is_dark_theme
        variant = "dark" if is_dark else "light"

        # Use custom opacity if set, otherwise auto-calculate
        if self.state.blur_opacity is not None:
            opacity = self.state.blur_opacity
        else:
            opacity = calculate_theme_opacity(palette, is_dark)

        exported_files = []

        # Export based on format selection
        if export_format in ("json", "all"):
            json_path = os.path.join(output_dir, f"palette-{variant}.json")
            source_file = os.path.basename(self.state.image_path)
            export_json(
                palette,
                json_path,
                blur_opacity=opacity,
                source_file=source_file,
                theme_name=theme_name,
                is_dark=is_dark,
                has_both_variants=False,
            )
            exported_files.append(json_path)

        if export_format in ("html", "all"):
            html_path = os.path.join(output_dir, f"palette_preview-{variant}.html")
            create_html_preview(
                palette,
                self.state.extracted_colors,
                html_path,
                is_dark,
            )
            exported_files.append(html_path)

        if export_format in ("zed", "all"):
            zed_path = os.path.join(output_dir, f"{theme_name}.json")
            zed_blur_path = os.path.join(output_dir, f"{theme_name}-blur.json")

            # Opaque theme
            zed_theme = generate_zed_theme(palette, theme_name, is_dark)
            with open(zed_path, "w") as f:
                f.write(zed_theme)
            exported_files.append(zed_path)

            # Blur theme
            zed_blur = generate_zed_theme(palette, theme_name, is_dark, opacity=opacity)
            with open(zed_blur_path, "w") as f:
                f.write(zed_blur)
            exported_files.append(zed_blur_path)

        self.notify(f"Exported {len(exported_files)} files to {output_dir}")
