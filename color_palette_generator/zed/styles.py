from ..opacity import opacity_to_hex, calculate_layered_opacities
from .syntax import build_syntax_styles


def build_zed_style(palette, is_dark, opacity=None):
    """Build the style dict for a Zed theme from a palette.

    Args:
        palette: The color palette dict
        is_dark: Whether this is a dark theme
        opacity: Optional opacity value (0.0-1.0) for transparent blur theme.
                 If None, creates opaque theme (ff alpha).
    """
    # Terminal foreground/dim_foreground are inverted (dim_fg shows low-contrast text)
    term_fg = palette["foreground_bright"]
    term_dim_fg = palette["background"]  # Inverted for low contrast

    # Calculate opacity hex values using layered transparency system
    if opacity is not None:
        layers = calculate_layered_opacities(opacity)
        target_alpha = opacity_to_hex(opacity)  # Full editor target
        global_alpha = opacity_to_hex(layers["global"])
        editor_alpha = opacity_to_hex(layers["editor_layer"])
        tab_bar_alpha = opacity_to_hex(layers["tab_bar_layer"])
        tab_alpha = opacity_to_hex(layers["tab_layer"])
        title_status_alpha = opacity_to_hex(layers["title_status"])
        transparent_alpha = "00"
    else:
        # Opaque theme - all fully opaque
        target_alpha = "ff"
        global_alpha = "ff"
        editor_alpha = "ff"
        tab_bar_alpha = "ff"
        tab_alpha = "ff"
        title_status_alpha = "ff"
        transparent_alpha = "ff"

    style = {
        "border": f"{palette['border'].hex}{'ff' if opacity is None else opacity_to_hex(0.4)}",
        "border.variant": f"{palette['border_variant'].hex}{'ff' if opacity is None else opacity_to_hex(0.4)}",
        "border.focused": f"{palette['border_focused'].hex}{'ff' if opacity is None else opacity_to_hex(0.4)}",
        "border.selected": f"{palette['border_selected'].hex}ff",
        "border.transparent": "#00000000",
        "border.disabled": f"{palette['border_disabled'].hex}ff",
        # Elevated surfaces (popups) - use full target opacity
        "elevated_surface.background": f"{palette['background_medium'].hex}{target_alpha}",
        # Surface - transparent (inherits from global)
        "surface.background": f"{palette['background_medium'].hex}{transparent_alpha}",
        # Global background - base layer for panels
        "background": f"{palette['background_light' if opacity is None else 'background_medium'].hex}{global_alpha}",
        "element.background": f"{palette['element'].hex}{'ff' if opacity is None else transparent_alpha}",
        "element.hover": f"{palette['element_hover'].hex}{'ff' if opacity is None else title_status_alpha}",
        "element.active": f"{palette['element_active'].hex}{'ff' if opacity is None else title_status_alpha}",
        "element.selected": f"{palette['element_selected'].hex}{'ff' if opacity is None else title_status_alpha}",
        "element.disabled": f"{palette['element_disabled'].hex}{'ff' if opacity is None else title_status_alpha}",
        "drop_target.background": f"{palette['element_hover'].hex}80",
        "ghost_element.background": "#00000000",
        "ghost_element.hover": f"{palette['element_hover'].hex}ff",
        "ghost_element.active": f"{palette['element_active'].hex}ff",
        "ghost_element.selected": f"{palette['element_selected'].hex}ff",
        "ghost_element.disabled": f"{palette['element_disabled'].hex}ff",
        "text": f"{palette['foreground_bright'].hex}ff",
        "text.muted": f"{palette['foreground'].hex}ff",
        "text.placeholder": f"{palette['foreground_dim'].hex}ff",
        "text.disabled": f"{palette['foreground_dim'].hex}ff",
        "text.accent": f"{palette['tertiary'].hex}ff",
        "icon": f"{palette['foreground_bright'].hex}ff",
        "icon.muted": f"{palette['foreground'].hex}ff",
        "icon.disabled": f"{palette['foreground_dim'].hex}ff",
        "icon.placeholder": f"{palette['foreground'].hex}ff",
        "icon.accent": f"{palette['tertiary'].hex}ff",
        # Title/status bars - standalone, no stacking
        "status_bar.background": f"{palette['background_light'].hex}{title_status_alpha}",
        "title_bar.background": f"{palette['background_light'].hex}{title_status_alpha}",
        "title_bar.inactive_background": f"{palette['background_light'].hex}{title_status_alpha}",
        "toolbar.background": f"{palette['background'].hex}{editor_alpha}",
        # Tab bar - stacks on global
        "tab_bar.background": f"{palette['background_medium'].hex}{tab_bar_alpha}",
        "tab.inactive_background": f"{palette['background_medium'].hex}{tab_alpha}",
        "tab.active_background": f"{palette['background'].hex}{target_alpha}",
        "search.match_background": f"{palette['tertiary'].hex}66",
        # Panel - transparent (inherits global)
        "panel.background": f"{palette['background_medium'].hex}{transparent_alpha}",
        "panel.focused_border": None,
        "pane.focused_border": None,
        "scrollbar.thumb.background": f"{palette['primary'].hex}4c",
        "scrollbar.thumb.hover_background": f"{palette['primary_variant'].hex}ff",
        "scrollbar.thumb.border": f"{palette['primary_variant'].hex}{'ff' if opacity is None else transparent_alpha}",
        "scrollbar.track.background": "#00000000",
        "scrollbar.track.border": f"{palette['primary'].hex}{'ff' if opacity is None else transparent_alpha}",
        "editor.foreground": f"{palette['foreground'].hex}ff",
        # Editor - stacks on global to reach target opacity
        "editor.background": f"{palette['background'].hex}{editor_alpha}",
        "editor.gutter.background": f"{palette['background'].hex}{editor_alpha}",
        "editor.subheader.background": f"{palette['background_medium'].hex}{editor_alpha}",
        "editor.active_line.background": f"{palette['background_medium'].hex}bf",
        "editor.highlighted_line.background": f"{palette['background_medium'].hex}ff",
        "editor.line_number": f"{palette['foreground_dim'].hex}ff",
        "editor.active_line_number": f"{palette['foreground_bright'].hex}ff",
        "editor.hover_line_number": f"{palette['foreground_dim'].hex}ff",
        "editor.invisible": f"{palette['foreground_dim'].hex}ff",
        "editor.wrap_guide": f"{palette['primary'].hex}0d",
        "editor.active_wrap_guide": f"{palette['primary'].hex}1a",
        "editor.document_highlight.read_background": f"{palette['tertiary'].hex}1a",
        "editor.document_highlight.write_background": f"{palette['primary'].hex}66",
        # Terminal - transparent (inherits from editor which stacks on global)
        "terminal.background": f"{palette['background'].hex}{transparent_alpha}",
        "terminal.foreground": f"{term_fg.hex}ff",
        "terminal.bright_foreground": f"{term_fg.hex}ff",
        "terminal.dim_foreground": f"{term_dim_fg.hex}ff",
        "terminal.ansi.black": f"{palette['black'].hex}ff",
        "terminal.ansi.bright_black": f"{palette['black_bright'].hex}ff",
        "terminal.ansi.dim_black": f"{palette['black_dim'].hex}ff",
        "terminal.ansi.red": f"{palette['red'].hex}ff",
        "terminal.ansi.bright_red": f"{palette['red_bright'].hex}ff",
        "terminal.ansi.dim_red": f"{palette['red_dim'].hex}ff",
        "terminal.ansi.green": f"{palette['green'].hex}ff",
        "terminal.ansi.bright_green": f"{palette['green_bright'].hex}ff",
        "terminal.ansi.dim_green": f"{palette['green_dim'].hex}ff",
        "terminal.ansi.yellow": f"{palette['yellow'].hex}ff",
        "terminal.ansi.bright_yellow": f"{palette['yellow_bright'].hex}ff",
        "terminal.ansi.dim_yellow": f"{palette['yellow_dim'].hex}ff",
        "terminal.ansi.blue": f"{palette['blue'].hex}ff",
        "terminal.ansi.bright_blue": f"{palette['blue_bright'].hex}ff",
        "terminal.ansi.dim_blue": f"{palette['blue_dim'].hex}ff",
        "terminal.ansi.magenta": f"{palette['magenta'].hex}ff",
        "terminal.ansi.bright_magenta": f"{palette['magenta_bright'].hex}ff",
        "terminal.ansi.dim_magenta": f"{palette['magenta_dim'].hex}ff",
        "terminal.ansi.cyan": f"{palette['cyan'].hex}ff",
        "terminal.ansi.bright_cyan": f"{palette['cyan_bright'].hex}ff",
        "terminal.ansi.dim_cyan": f"{palette['cyan_dim'].hex}ff",
        "terminal.ansi.white": f"{palette['white'].hex}ff",
        "terminal.ansi.bright_white": f"{palette['white_bright'].hex}ff",
        "terminal.ansi.dim_white": f"{palette['white_dim'].hex}ff",
        "link_text.hover": f"{palette['info'].hex}ff",
        "version_control.added": f"{palette['green'].hex}ff",
        "version_control.modified": f"{palette['yellow'].hex}ff",
        "version_control.deleted": f"{palette['red'].hex}ff",
        "version_control.conflict_marker.ours": f"{palette['success'].hex}1a",
        "version_control.conflict_marker.theirs": f"{palette['tertiary'].hex}1a",
        "conflict": f"{palette['warning'].hex}ff",
        "conflict.background": f"{palette['warning'].hex}1a",
        "conflict.border": f"{palette['yellow_dim'].hex}c2",
        "created": f"{palette['success'].hex}ff",
        "created.background": f"{palette['success'].hex}1a",
        "created.border": f"{palette['green_dim'].hex}c2",
        "deleted": f"{palette['error'].hex}ff",
        "deleted.background": f"{palette['error'].hex}1a",
        "deleted.border": f"{palette['red_dim'].hex}c2",
        "error": f"{palette['error'].hex}ff",
        "error.background": f"{palette['error'].hex}1a",
        "error.border": f"{palette['red_dim'].hex}c2",
        "hidden": f"{palette['foreground_dim'].hex}ff",
        "hidden.background": f"{palette['background_disabled'].hex}1a",
        "hidden.border": f"{palette['muted'].hex}ff",
        "hint": f"{palette['blue_bright'].hex}ff",
        "hint.background": f"{palette['secondary_variant'].hex}1a",
        "hint.border": f"{palette['secondary_variant'].hex}ff",
        "ignored": f"{palette['foreground_dim'].hex}ff",
        "ignored.background": f"{palette['background_disabled'].hex}1a",
        "ignored.border": f"{palette['primary'].hex}ff",
        "info": f"{palette['info'].hex}ff",
        "info.background": f"{palette['info'].hex}1a",
        "info.border": f"{palette['blue_dim'].hex}ff",
        "modified": f"{palette['warning'].hex}ff",
        "modified.background": f"{palette['warning'].hex}1a",
        "modified.border": f"{palette['yellow_dim'].hex}c2",
        "predictive": f"{palette['cyan_bright'].hex}ff",
        "predictive.background": f"{palette['cyan_bright'].hex}1a",
        "predictive.border": f"{palette['green_dim'].hex}c2",
        "renamed": f"{palette['tertiary'].hex}ff",
        "renamed.background": f"{palette['tertiary'].hex}1a",
        "renamed.border": f"{palette['secondary_variant'].hex}ff",
        "success": f"{palette['success'].hex}ff",
        "success.background": f"{palette['success'].hex}1a",
        "success.border": f"{palette['green_dim'].hex}c2",
        "unreachable": f"{palette['foreground'].hex}ff",
        "unreachable.background": f"{palette['primary'].hex}1a",
        "unreachable.border": f"{palette['primary'].hex}ff",
        "warning": f"{palette['warning'].hex}ff",
        "warning.background": f"{palette['warning'].hex}1a",
        "warning.border": f"{palette['yellow_dim'].hex}c2",
        "players": [
            {
                "cursor": f"{palette['tertiary'].hex}ff",
                "background": f"{palette['tertiary'].hex}ff",
                "selection": f"{palette['tertiary'].hex}3d",
            },
            {
                "cursor": f"{palette['magenta'].hex}ff",
                "background": f"{palette['magenta'].hex}ff",
                "selection": f"{palette['magenta'].hex}3d",
            },
            {
                "cursor": f"{palette['cyan'].hex}ff",
                "background": f"{palette['cyan'].hex}ff",
                "selection": f"{palette['cyan'].hex}3d",
            },
            {
                "cursor": f"{palette['error'].hex}ff",
                "background": f"{palette['error'].hex}ff",
                "selection": f"{palette['error'].hex}3d",
            },
            {
                "cursor": f"{palette['warning'].hex}ff",
                "background": f"{palette['warning'].hex}ff",
                "selection": f"{palette['warning'].hex}3d",
            },
            {
                "cursor": f"{palette['success'].hex}ff",
                "background": f"{palette['success'].hex}ff",
                "selection": f"{palette['success'].hex}3d",
            },
        ],
        "syntax": build_syntax_styles(palette),
    }

    # Add blur appearance for transparent themes
    if opacity is not None:
        style["background.appearance"] = "blurred"

    return style
