# Contrast requirements
MIN_TEXT_CONTRAST = 5.0  # Main text against bg AND bg_light
MIN_DIM_CONTRAST = 4.0  # Dim text against bg AND bg_light
MIN_TERMINAL_CONTRAST = 4.0  # All terminal colors 1-15
MIN_SEMANTIC_CONTRAST = 4.5  # Error, warning, success, info

# Saturation limits to avoid gaudy colors
MAX_BG_SATURATION = 35  # Backgrounds shouldn't be too colorful
MAX_FG_SATURATION = 25  # Foregrounds should be near-neutral
MAX_ACCENT_SATURATION = 75  # Accents can be vibrant but not neon
