import json

from ..opacity import opacity_to_hex


def export_json(palette, filepath, blur_opacity=None):
    """Export palette as JSON with all 24 terminal colors and blur opacity"""
    data = {k: v.hex for k, v in palette.items()}
    if blur_opacity is not None:
        data["_blur_opacity"] = {
            "float": round(blur_opacity, 2),
            "hex": opacity_to_hex(blur_opacity),
        }
    data["_alpha_suggestion"] = {
        "background": "E6",
        "selection": "80",
    }
    data["_note"] = (
        "24 terminal colors: black/red/green/yellow/blue/magenta/cyan/white with _bright and _dim variants"
    )
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
