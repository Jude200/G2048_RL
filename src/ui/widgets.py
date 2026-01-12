"""Custom UI widgets for the 2048 game"""

import customtkinter as ctk
from typing import Callable, Optional
from src.utils.constants import TILE_SIZE, PADDING

class TileWidget(ctk.CTkLabel):
    """Represents a visual tile in the game"""
    
    def __init__(self, parent, value: int = 0, row: int = 0, col: int = 0, **kwargs):
        """
        Initialize a tile widget.
        
        Args:
            parent: Parent widget
            value: Tile value
            row: Grid row position
            col: Grid column position
        """
        super().__init__(parent, **kwargs)
        self.value = value
        self.row = row
        self.col = col
        self.previous_value = 0
        self.update_display()
    
    def update_display(self, value: int = None):
        """Update the tile display with animation"""
        if value is not None:
            self.previous_value = self.value
            self.value = value
        
        from .styles import get_text_color, get_bg_color
        
        # Display
        if self.value == 0:
            self.configure(text="", fg_color=get_bg_color(self.value))
        else:
            self.configure(text=str(self.value))
        
        # Set colors based on value with improved styling
        bg_color = get_bg_color(self.value)
        text_color = get_text_color(self.value)
        
        # Dynamic font size based on value
        font_size = 36
        if self.value >= 1024:
            font_size = 28
        elif self.value >= 128:
            font_size = 32
        
        self.configure(
            fg_color=bg_color,
            text_color=text_color,
            font=("Segoe UI", font_size, "bold"),
            corner_radius=8
        )

class ScoreDisplay(ctk.CTkFrame):
    """Widget to display score and best score"""
    
    def __init__(self, parent, **kwargs):
        from .styles import SCORE_BOX_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, SCORE_FONT, SCORE_VALUE_FONT
        
        # Remove fg_color and corner_radius from kwargs if present, then set them
        kwargs.pop('fg_color', None)
        kwargs.pop('corner_radius', None)
        super().__init__(parent, fg_color=SCORE_BOX_COLOR, corner_radius=8, **kwargs)
        
        # Score container
        score_container = ctk.CTkFrame(self, fg_color=SCORE_BOX_COLOR)
        score_container.pack(side="left", padx=15, pady=0, fill="both", expand=True)
        
        ctk.CTkLabel(score_container, text="Score", font=SCORE_FONT, text_color=TEXT_SECONDARY).pack(pady=0)
        self.score_label = ctk.CTkLabel(score_container, text="0", font=SCORE_VALUE_FONT, text_color=TEXT_PRIMARY)
        self.score_label.pack(pady=1)
        
        # Separator
        separator = ctk.CTkFrame(self, fg_color="#404040", width=2)
        separator.pack(side="left", fill="y", padx=8)
        
        # Best score container
        best_container = ctk.CTkFrame(self, fg_color=SCORE_BOX_COLOR)
        best_container.pack(side="left", padx=15, pady=0, fill="both", expand=True)
        
        ctk.CTkLabel(best_container, text="Best", font=SCORE_FONT, text_color=TEXT_SECONDARY).pack(pady=0)
        self.best_label = ctk.CTkLabel(best_container, text="0", font=SCORE_VALUE_FONT, text_color=TEXT_PRIMARY)
        self.best_label.pack(pady=1)
    
    def update_score(self, score: int, best: int):
        """Update score displays"""
        self.score_label.configure(text=str(score))
        self.best_label.configure(text=str(best))

class BoardWidget(ctk.CTkFrame):
    """The game board widget"""
    
    def __init__(self, parent, size: int = 4, **kwargs):
        from .styles import BOARD_BG_COLOR
        
        # Remove fg_color and corner_radius from kwargs if present, then set them
        kwargs.pop('fg_color', None)
        kwargs.pop('corner_radius', None)
        super().__init__(parent, fg_color=BOARD_BG_COLOR, corner_radius=12, **kwargs)
        self.size = size
        self.tiles = {}
        self._create_tiles()
    
    def _create_tiles(self):
        """Create the tile grid with improved spacing"""
        for i in range(self.size):
            for j in range(self.size):
                tile = TileWidget(self, value=0, row=i, col=j, 
                                 width=TILE_SIZE, height=TILE_SIZE,
                                 corner_radius=8)
                tile.grid(row=i, column=j, padx=PADDING, pady=PADDING)
                self.tiles[(i, j)] = tile
    
    def update_board(self, grid):
        """Update board display with new grid values"""
        for i in range(self.size):
            for j in range(self.size):
                self.tiles[(i, j)].update_display(grid[i][j])

