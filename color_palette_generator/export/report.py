from ..color import contrast_ratio
from ..constants import (
    MIN_TEXT_CONTRAST,
    MIN_DIM_CONTRAST,
    MIN_TERMINAL_CONTRAST,
    MIN_SEMANTIC_CONTRAST,
)


def generate_readability_report(palette, is_dark_theme):
    """Generate a detailed readability report for inspection"""
    bg = palette["background"]
    bg_light = palette["background_light"]

    report = []
    report.append("=" * 70)
    report.append("READABILITY REPORT")
    report.append("=" * 70)
    report.append(f"Theme: {'DARK' if is_dark_theme else 'LIGHT'}")
    bg_medium = palette["background_medium"]
    report.append(
        f"Background:       {bg.hex} (L: {bg.hsl[2]:.1f}%, S: {bg.hsl[1]:.1f}%)"
    )
    report.append(
        f"Background Med:   {bg_medium.hex} (L: {bg_medium.hsl[2]:.1f}%, S: {bg_medium.hsl[1]:.1f}%)"
    )
    report.append(
        f"Background Light: {bg_light.hex} (L: {bg_light.hsl[2]:.1f}%, S: {bg_light.hsl[1]:.1f}%)"
    )
    report.append("")

    # Check categories
    categories = [
        ("FOREGROUND (bright)", ["foreground_bright"], MIN_TEXT_CONTRAST),
        ("FOREGROUND (main)", ["foreground", "foreground_medium"], MIN_TEXT_CONTRAST),
        ("FOREGROUND (dim)", ["foreground_dim"], MIN_DIM_CONTRAST),
        (
            "ACCENTS",
            ["primary", "primary_variant", "secondary", "secondary_variant"],
            MIN_TERMINAL_CONTRAST,
        ),
        ("HIGHLIGHT", ["tertiary"], MIN_SEMANTIC_CONTRAST),
        ("SEMANTIC", ["error", "warning", "success", "info"], MIN_SEMANTIC_CONTRAST),
        (
            "TERMINAL BASE",
            ["red", "green", "yellow", "blue", "magenta", "cyan", "white"],
            MIN_TERMINAL_CONTRAST,
        ),
        (
            "TERMINAL BRIGHT",
            [
                "red_bright",
                "green_bright",
                "yellow_bright",
                "blue_bright",
                "magenta_bright",
                "cyan_bright",
                "white_bright",
            ],
            MIN_TERMINAL_CONTRAST,
        ),
        (
            "TERMINAL DIM",
            [
                "red_dim",
                "green_dim",
                "yellow_dim",
                "blue_dim",
                "magenta_dim",
                "cyan_dim",
                "white_dim",
            ],
            MIN_TERMINAL_CONTRAST,
        ),
    ]

    issues = []

    for cat_name, keys, min_contrast in categories:
        report.append(f"\n{cat_name} (min: {min_contrast}:1)")
        report.append("-" * 50)
        for key in keys:
            if key not in palette:
                continue
            c = palette[key]
            cr_bg = contrast_ratio(c.luminance, bg.luminance)
            cr_bg_light = contrast_ratio(c.luminance, bg_light.luminance)
            min_cr = min(cr_bg, cr_bg_light)

            status = "✓" if min_cr >= min_contrast else "✗ FAIL"
            if min_cr < min_contrast:
                issues.append((key, c.hex, min_cr, min_contrast))

            report.append(
                f"  {key:14} {c.hex}  vs bg: {cr_bg:4.1f}:1  vs bg_light: {cr_bg_light:4.1f}:1  {status}"
            )

    report.append("\n" + "=" * 70)
    if issues:
        report.append(f"ISSUES FOUND: {len(issues)}")
        for key, hex_val, achieved, required in issues:
            report.append(
                f"  - {key}: {hex_val} has {achieved:.1f}:1, needs {required}:1"
            )
    else:
        report.append("ALL COLORS PASS CONTRAST REQUIREMENTS ✓")
    report.append("=" * 70)

    return "\n".join(report), issues


def print_palette(palette, is_dark_theme):
    """Print palette info"""
    bg = palette["background"]

    print("\n" + "=" * 60)
    print(f"FUNCTIONAL COLOR PALETTE ({'DARK' if is_dark_theme else 'LIGHT'} THEME)")
    print("=" * 60)

    categories = [
        ("BACKGROUNDS", ["background", "background_light"]),
        ("FOREGROUNDS", ["foreground", "foreground_dim"]),
        ("ACCENTS", ["primary", "secondary", "tertiary", "muted", "selection"]),
        ("SEMANTIC", ["error", "warning", "success", "info"]),
        (
            "TERMINAL (Base)",
            ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"],
        ),
        (
            "TERMINAL (Bright)",
            [
                "black_bright",
                "red_bright",
                "green_bright",
                "yellow_bright",
                "blue_bright",
                "magenta_bright",
                "cyan_bright",
                "white_bright",
            ],
        ),
        (
            "TERMINAL (Dim)",
            [
                "black_dim",
                "red_dim",
                "green_dim",
                "yellow_dim",
                "blue_dim",
                "magenta_dim",
                "cyan_dim",
                "white_dim",
            ],
        ),
    ]

    for cat_name, keys in categories:
        print(f"\n{cat_name}:")
        for key in keys:
            if key in palette:
                c = palette[key]
                contrast = contrast_ratio(c.luminance, bg.luminance)
                print(f"  {key:18} {c.hex}  (contrast: {contrast:.1f}:1)")
