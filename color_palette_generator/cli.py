import argparse
import os

from .palette import generate_functional_palette
from .opacity import calculate_theme_opacity
from .export import export_json, create_html_preview, generate_readability_report, print_palette
from .zed import generate_zed_themes


def main():
    parser = argparse.ArgumentParser(
        description="Generate color palettes and Zed themes from images"
    )
    parser.add_argument("image_path", help="Path to the source image")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=None,
        help="Output directory (default: same as image)",
    )
    parser.add_argument(
        "--opacity",
        type=float,
        default=None,
        help="Override blur theme opacity (0.0-1.0). If not set, auto-calculates optimal value.",
    )

    args = parser.parse_args()

    image_path = args.image_path
    output_dir = args.output_dir or os.path.dirname(image_path) or "."
    override_opacity = args.opacity

    os.makedirs(output_dir, exist_ok=True)

    print(f"Analyzing: {image_path}")

    # Generate both dark and light palettes
    dark_palette, dark_extracted, _, _ = generate_functional_palette(
        image_path, force_theme="dark"
    )
    light_palette, light_extracted, _, _ = generate_functional_palette(
        image_path, force_theme="light"
    )

    # Print and export dark theme
    print_palette(dark_palette, is_dark_theme=True)
    dark_report, dark_issues = generate_readability_report(
        dark_palette, is_dark_theme=True
    )
    print("\n" + dark_report)

    # Print and export light theme
    print_palette(light_palette, is_dark_theme=False)
    light_report, light_issues = generate_readability_report(
        light_palette, is_dark_theme=False
    )
    print("\n" + light_report)

    # Export paths
    # Get theme name from image filename (without extension)
    theme_name = os.path.splitext(os.path.basename(image_path))[0]

    dark_json_path = os.path.join(output_dir, "palette-dark.json")
    dark_html_path = os.path.join(output_dir, "palette_preview-dark.html")
    dark_report_path = os.path.join(output_dir, "readability_report-dark.txt")

    light_json_path = os.path.join(output_dir, "palette-light.json")
    light_html_path = os.path.join(output_dir, "palette_preview-light.html")
    light_report_path = os.path.join(output_dir, "readability_report-light.txt")

    zed_path = os.path.join(output_dir, f"{theme_name}.json")
    zed_blur_path = os.path.join(output_dir, f"{theme_name}-blur.json")

    # Calculate opacity for blur theme (needed for palette export too)
    if override_opacity is not None:
        dark_opacity = override_opacity
        light_opacity = override_opacity
    else:
        dark_opacity = calculate_theme_opacity(dark_palette, is_dark_theme=True)
        light_opacity = calculate_theme_opacity(light_palette, is_dark_theme=False)

    # Export dark theme files
    export_json(dark_palette, dark_json_path, blur_opacity=dark_opacity)
    create_html_preview(
        dark_palette, dark_extracted, dark_html_path, is_dark_theme=True
    )
    with open(dark_report_path, "w") as f:
        f.write(dark_report)

    # Export light theme files
    export_json(light_palette, light_json_path, blur_opacity=light_opacity)
    create_html_preview(
        light_palette, light_extracted, light_html_path, is_dark_theme=False
    )
    with open(light_report_path, "w") as f:
        f.write(light_report)

    # Export opaque Zed theme
    zed_theme = generate_zed_themes(dark_palette, light_palette, theme_name)
    with open(zed_path, "w") as f:
        f.write(zed_theme)

    # Export blur Zed theme
    zed_blur_theme = generate_zed_themes(
        dark_palette,
        light_palette,
        theme_name,
        dark_opacity=dark_opacity,
        light_opacity=light_opacity,
    )
    with open(zed_blur_path, "w") as f:
        f.write(zed_blur_theme)

    print("\n" + "=" * 60)
    print("Exported:")
    print(f"  - {dark_json_path}")
    print(f"  - {dark_html_path}")
    print(f"  - {dark_report_path}")
    print(f"  - {light_json_path}")
    print(f"  - {light_html_path}")
    print(f"  - {light_report_path}")
    print(f"  - {zed_path} (contains '{theme_name} Dark' and '{theme_name} Light')")
    print(
        f"  - {zed_blur_path} (contains '{theme_name} Dark Blur' and '{theme_name} Light Blur')"
    )
    print(f"\nBlur opacity: dark={dark_opacity:.2f}, light={light_opacity:.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
