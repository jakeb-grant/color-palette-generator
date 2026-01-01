import colorsys


def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hsl(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    h, lightness, s = colorsys.rgb_to_hls(r, g, b)
    return (h * 360, s * 100, lightness * 100)


def hsl_to_rgb(h, s, lightness):
    h, s, lightness = h / 360, s / 100, lightness / 100
    r, g, b = colorsys.hls_to_rgb(h, lightness, s)
    return (int(r * 255), int(g * 255), int(b * 255))
