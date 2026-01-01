def build_syntax_styles(palette):
    """Build syntax highlighting styles from palette.

    Returns a dict mapping syntax token types to their style definitions.
    """
    return {
        "attribute": {
            "color": f"{palette['tertiary'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "boolean": {
            "color": f"{palette['yellow'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "comment": {
            "color": f"{palette['foreground_dim'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "comment.doc": {
            "color": f"{palette['foreground_medium'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "constant": {
            "color": f"{palette['yellow'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "constructor": {
            "color": f"{palette['blue_dim'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "embedded": {
            "color": f"{palette['foreground_bright'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "emphasis": {
            "color": f"{palette['tertiary'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "emphasis.strong": {
            "color": f"{palette['yellow'].hex}ff",
            "font_style": None,
            "font_weight": 700,
        },
        "enum": {
            "color": f"{palette['error'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "function": {
            "color": f"{palette['cyan_dim'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "hint": {
            "color": f"{palette['blue_bright'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "keyword": {
            "color": f"{palette['magenta'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "label": {
            "color": f"{palette['tertiary'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "link_text": {
            "color": f"{palette['cyan_dim'].hex}ff",
            "font_style": "normal",
            "font_weight": None,
        },
        "link_uri": {
            "color": f"{palette['cyan'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "namespace": {
            "color": f"{palette['foreground_bright'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "number": {
            "color": f"{palette['yellow'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "operator": {
            "color": f"{palette['cyan'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "predictive": {
            "color": f"{palette['cyan_bright'].hex}ff",
            "font_style": "italic",
            "font_weight": None,
        },
        "preproc": {
            "color": f"{palette['foreground_bright'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "primary": {
            "color": f"{palette['foreground'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "property": {
            "color": f"{palette['error'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "punctuation": {
            "color": f"{palette['foreground'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "punctuation.bracket": {
            "color": f"{palette['foreground_medium'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "punctuation.delimiter": {
            "color": f"{palette['foreground_medium'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "punctuation.list_marker": {
            "color": f"{palette['error'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "punctuation.markup": {
            "color": f"{palette['error'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "punctuation.special": {
            "color": f"{palette['red'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "selector": {
            "color": f"{palette['yellow'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "selector.pseudo": {
            "color": f"{palette['tertiary'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "string": {
            "color": f"{palette['success'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "string.escape": {
            "color": f"{palette['foreground_medium'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "string.regex": {
            "color": f"{palette['yellow'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "string.special": {
            "color": f"{palette['yellow'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "string.special.symbol": {
            "color": f"{palette['yellow'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "tag": {
            "color": f"{palette['tertiary'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "text.literal": {
            "color": f"{palette['success'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "title": {
            "color": f"{palette['error'].hex}ff",
            "font_style": None,
            "font_weight": 400,
        },
        "type": {
            "color": f"{palette['cyan'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "variable": {
            "color": f"{palette['foreground'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "variable.special": {
            "color": f"{palette['yellow'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
        "variant": {
            "color": f"{palette['blue_dim'].hex}ff",
            "font_style": None,
            "font_weight": None,
        },
    }
