"""Tile class representing a single tile on the board"""

class Tile:
    """Represents a single tile in the 2048 game"""
    
    def __init__(self, value: int = 0, row: int = 0, col: int = 0):
        """
        Initialize a tile.
        
        Args:
            value: The numeric value of the tile (default 0 for empty)
            row: Row position on the board
            col: Column position on the board
        """
        self.value = value
        self.row = row
        self.col = col
        self.merged_this_turn = False
    
    def __repr__(self) -> str:
        return f"Tile(value={self.value}, row={self.row}, col={self.col})"
    
    def __eq__(self, other) -> bool:
        """Check if two tiles have the same value"""
        if isinstance(other, Tile):
            return self.value == other.value
        return self.value == other
    
    def is_empty(self) -> bool:
        """Check if tile is empty (value is 0)"""
        return self.value == 0
    
    def reset_merge_flag(self):
        """Reset the merge flag for the next turn"""
        self.merged_this_turn = False
    
    def merge(self, other: "Tile") -> "Tile":
        """
        Merge this tile with another.
        
        Args:
            other: The tile to merge with
            
        Returns:
            A new tile with the merged value
        """
        if self.value == other.value:
            merged = Tile(self.value * 2, self.row, self.col)
            merged.merged_this_turn = True
            return merged
        return None
