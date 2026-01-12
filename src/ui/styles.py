"""Game styles and themes"""

# Modern color theme for tiles with gradients
TILE_COLORS = {
    0: "#e8dcc8",
    2: "#fffbf0",
    4: "#fff9e6",
    8: "#ffd966",
    16: "#ffb952",
    32: "#ffa64d",
    64: "#ff9340",
    128: "#ffeb3b",
    256: "#ffd700",
    512: "#ffc700",
    1024: "#ffb700",
    2048: "#ffa700",
    4096: "#ff6f00",
    8192: "#e65100",
}

TEXT_COLORS = {
    0: "#9e9e9e",
    2: "#776e65",
    4: "#776e65",
    8: "#2c2c2c",
    16: "#2c2c2c",
    32: "#2c2c2c",
    64: "#ffffff",
    128: "#ffffff",
    256: "#ffffff",
    512: "#ffffff",
    1024: "#ffffff",
    2048: "#ffffff",
    4096: "#ffffff",
    8192: "#ffffff",
}

# Default text color for higher values
DEFAULT_TEXT_COLOR = "#ffffff"

# Font configuration - Modern and clean
TITLE_FONT = ("Segoe UI", 40, "bold")
SUBTITLE_FONT = ("Segoe UI", 12)
SCORE_FONT = ("Segoe UI", 12, "bold")
SCORE_VALUE_FONT = ("Segoe UI", 20, "bold")
TILE_FONT = ("Segoe UI", 36, "bold")
BUTTON_FONT = ("Segoe UI", 12, "bold")
INFO_FONT = ("Segoe UI", 10)

# Window configuration - Modern gradient theme
BG_COLOR = "#1a1a1a"
HEADER_COLOR = "#2d2d2d"
BOARD_BG_COLOR = "#2a2a2a"
SCORE_BOX_COLOR = "#323232"
BUTTON_COLOR = "#ff9800"
BUTTON_HOVER_COLOR = "#ffa726"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#b0b0b0"
WINDOW_TITLE = "2048 Game"
ACCENT_COLOR = "#ffa726"

def get_text_color(value: int) -> str:
    """Get text color based on tile value"""
    if value in TEXT_COLORS:
        return TEXT_COLORS[value]
    return DEFAULT_TEXT_COLOR

def get_bg_color(value: int) -> str:
    """Get background color based on tile value"""
    return TILE_COLORS.get(value, TILE_COLORS[8192])
