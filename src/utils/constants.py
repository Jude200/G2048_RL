"""Game constants and configuration"""

# Board configuration
BOARD_SIZE = 4
WINNING_TILE = 2048

# Tile configuration
MIN_TILE_VALUE = 2
SPAWN_TILE_VALUES = [2, 4]
SPAWN_PROBABILITY = 0.8  # 80% chance for 2, 20% for 4

# UI configuration
TILE_SIZE = 85
PADDING = 8
WINDOW_WIDTH = BOARD_SIZE * TILE_SIZE + (BOARD_SIZE + 1) * PADDING
WINDOW_HEIGHT = WINDOW_WIDTH + 100  # Extra space for buttons/score

# Color scheme
COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
    4096: "#3c3422",
    8192: "#3c3422",
}

TEXT_COLOR = {
    2: "#776e65",
    4: "#776e65",
    8: "#f9f6f2",
    16: "#f9f6f2",
    32: "#f9f6f2",
    64: "#f9f6f2",
    128: "#f9f6f2",
    256: "#f9f6f2",
    512: "#f9f6f2",
    1024: "#f9f6f2",
    2048: "#f9f6f2",
    4096: "#f9f6f2",
    8192: "#f9f6f2",
}

# Game settings
ANIMATION_DURATION = 100  # milliseconds
FPS = 60
SAVE_FILE = "saves/game_save.json"
