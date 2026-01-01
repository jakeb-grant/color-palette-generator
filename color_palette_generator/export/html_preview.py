HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Color Palette Preview</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'SF Mono', 'Fira Code', monospace;
            background: {bg};
            color: {fg};
            padding: 40px;
            min-height: 100vh;
        }
        h1 { margin-bottom: 10px; font-weight: 400; }
        .theme-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            margin-bottom: 30px;
            background: {bg_light};
            color: {fg_dim};
        }
        h2 {
            margin: 30px 0 15px 0;
            font-weight: 400;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: {fg_dim};
        }
        .palette-section {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 20px;
        }
        .color-card {
            width: 160px;
            border-radius: 8px;
            overflow: hidden;
            background: {bg_light};
        }
        .color-swatch {
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 500;
        }
        .color-info {
            padding: 12px;
            font-size: 11px;
        }
        .color-name {
            font-weight: 600;
            margin-bottom: 4px;
        }
        .color-hex {
            opacity: 0.7;
        }
        .terminal-grid {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 10px;
        }
        .terminal-color {
            aspect-ratio: 1;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 600;
        }
        .preview-box {
            background: {bg_light};
            border-radius: 12px;
            padding: 25px;
            margin-top: 30px;
        }
        .preview-box h3 {
            margin-bottom: 15px;
            font-weight: 400;
        }
        .sample-text { margin: 8px 0; }
        .dim { color: {fg_dim}; }
        .primary { color: {primary}; }
        .secondary { color: {secondary}; }
        .blur-demo {
            background: {bg}E6;
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
            border: 1px solid {muted};
        }
        .contrast-test {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 30px;
        }
        .contrast-box {
            padding: 20px;
            border-radius: 8px;
        }
        .contrast-box h4 {
            margin-bottom: 10px;
            font-weight: 500;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .contrast-box p {
            margin: 5px 0;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>Functional Color Palette</h1>
    <div class="theme-badge">{theme_type} Theme</div>

    <h2>Backgrounds & Foregrounds</h2>
    <div class="palette-section">
        {bg_fg_cards}
    </div>

    <h2>Element Backgrounds</h2>
    <div class="palette-section">
        {element_cards}
    </div>

    <h2>Borders</h2>
    <div class="palette-section">
        {border_cards}
    </div>

    <h2>Accent Colors</h2>
    <div class="palette-section">
        {accent_cards}
    </div>

    <h2>Semantic Colors</h2>
    <div class="palette-section">
        {semantic_cards}
    </div>

    <h2>Terminal Colors (0-15)</h2>
    <div class="terminal-grid">
        {terminal_colors}
    </div>

    <h2>Readability Test</h2>
    <div class="contrast-test">
        <div class="contrast-box" style="background: {bg}">
            <h4>On Background</h4>
            <p style="color: {fg_bright}">Foreground bright (headings)</p>
            <p style="color: {fg}">Foreground text (primary)</p>
            <p style="color: {fg_medium}">Foreground medium (secondary)</p>
            <p style="color: {fg_dim}">Foreground dim (comments)</p>
            <p style="color: {error}">Error message</p>
            <p style="color: {warning}">Warning message</p>
            <p style="color: {success}">Success message</p>
            <p style="color: {info}">Info message</p>
        </div>
        <div class="contrast-box" style="background: {bg_light}">
            <h4>On Background Light</h4>
            <p style="color: {fg_bright}">Foreground bright (headings)</p>
            <p style="color: {fg}">Foreground text (primary)</p>
            <p style="color: {fg_medium}">Foreground medium (secondary)</p>
            <p style="color: {fg_dim}">Foreground dim (comments)</p>
            <p style="color: {error}">Error message</p>
            <p style="color: {warning}">Warning message</p>
            <p style="color: {success}">Success message</p>
            <p style="color: {info}">Info message</p>
        </div>
    </div>

    <div class="preview-box">
        <h3>Terminal Preview</h3>
        <p style="color: {red}">red: Error output</p>
        <p style="color: {green}">green: Success / git additions</p>
        <p style="color: {yellow}">yellow: Warnings / strings</p>
        <p style="color: {blue}">blue: Info / directories</p>
        <p style="color: {magenta}">magenta: Keywords / magenta</p>
        <p style="color: {cyan}">cyan: Cyan / special</p>
    </div>
</body>
</html>"""


def _make_card(name, color):
    text_color = "#ffffff" if color.luminance < 0.5 else "#000000"
    return f"""<div class="color-card">
        <div class="color-swatch" style="background: {color.hex}; color: {text_color}">Aa</div>
        <div class="color-info">
            <div class="color-name">{name}</div>
            <div class="color-hex">{color.hex}</div>
        </div>
    </div>"""


def _make_terminal_color(name, color):
    text_color = "#ffffff" if color.luminance < 0.5 else "#000000"
    return f'<div class="terminal-color" style="background: {color.hex}; color: {text_color}">{name}</div>'


def create_html_preview(palette, extracted_colors, output_path, is_dark_theme):
    """Create an HTML preview of the palette"""
    html = HTML_TEMPLATE

    bg_fg_names = [
        "background",
        "background_medium",
        "background_light",
        "background_disabled",
        "foreground_bright",
        "foreground",
        "foreground_medium",
        "foreground_dim",
    ]
    element_names = [
        "element",
        "element_hover",
        "element_active",
        "element_selected",
        "element_disabled",
    ]
    border_names = [
        "border",
        "border_variant",
        "border_focused",
        "border_selected",
        "border_disabled",
    ]
    accent_names = [
        "primary",
        "primary_variant",
        "secondary",
        "secondary_variant",
        "tertiary",
        "muted",
        "selection",
    ]
    semantic_names = ["error", "warning", "success", "info"]
    terminal_color_names = [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    ]

    replacements = {
        "{bg}": palette["background"].hex,
        "{bg_light}": palette["background_light"].hex,
        "{fg}": palette["foreground"].hex,
        "{fg_bright}": palette["foreground_bright"].hex,
        "{fg_medium}": palette["foreground_medium"].hex,
        "{fg_dim}": palette["foreground_dim"].hex,
        "{primary}": palette["primary"].hex,
        "{secondary}": palette["secondary"].hex,
        "{muted}": palette["muted"].hex,
        "{error}": palette["error"].hex,
        "{warning}": palette["warning"].hex,
        "{success}": palette["success"].hex,
        "{info}": palette["info"].hex,
        "{theme_type}": "Dark" if is_dark_theme else "Light",
    }

    # Add terminal colors
    for name in terminal_color_names:
        if name in palette:
            replacements[f"{{{name}}}"] = palette[name].hex

    for old, new in replacements.items():
        html = html.replace(old, new)

    html = html.replace(
        "{bg_fg_cards}", "\n".join(_make_card(n, palette[n]) for n in bg_fg_names)
    )
    html = html.replace(
        "{element_cards}", "\n".join(_make_card(n, palette[n]) for n in element_names)
    )
    html = html.replace(
        "{border_cards}", "\n".join(_make_card(n, palette[n]) for n in border_names)
    )
    html = html.replace(
        "{accent_cards}", "\n".join(_make_card(n, palette[n]) for n in accent_names)
    )
    html = html.replace(
        "{semantic_cards}", "\n".join(_make_card(n, palette[n]) for n in semantic_names)
    )

    # Generate terminal color grid with base + bright variants
    terminal_grid = []
    for name in terminal_color_names:
        if name in palette:
            terminal_grid.append(_make_terminal_color(name, palette[name]))
    for name in terminal_color_names:
        bright_name = f"{name}_bright"
        if bright_name in palette:
            terminal_grid.append(_make_terminal_color(bright_name, palette[bright_name]))
    for name in terminal_color_names:
        dim_name = f"{name}_dim"
        if dim_name in palette:
            terminal_grid.append(_make_terminal_color(dim_name, palette[dim_name]))
    html = html.replace("{terminal_colors}", "\n".join(terminal_grid))

    with open(output_path, "w") as f:
        f.write(html)
