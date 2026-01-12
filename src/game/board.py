"""Board class managing the game grid"""

import random
import numpy as np
from typing import List, Tuple, Optional
from src.utils.constants import BOARD_SIZE, SPAWN_TILE_VALUES, SPAWN_PROBABILITY
from src.utils.logger import get_logger
from .tile import Tile

logger = get_logger(__name__)

class Board:
    """Manages the 2048 game board"""
    
    def __init__(self, size: int = BOARD_SIZE):
        """
        Initialize the game board.
        
        Args:
            size: The size of the board (default 4x4)
        """
        self.size = size
        self.grid: np.ndarray = np.zeros((size, size), dtype=np.int32)
        self.previous_grid: Optional[np.ndarray] = None
        self.merged_values = []
        
        self.score = 0
        self.move_count = 0
        self._add_random_tile()
        self._add_random_tile()
    
    def _add_random_tile(self):
        """Add a random tile (2 or 4) to an empty cell"""
        empty_cells = self._get_empty_cells()
        
        if not empty_cells:
            logger.warning("No empty cells available")
            return
        
        row, col = random.choice(empty_cells)
        value = 4 if random.random() > SPAWN_PROBABILITY else 2
        self.grid[row][col] = value
        logger.debug(f"Added tile with value {value} at ({row}, {col})")
    
    def _get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get list of all empty cells"""
        empty_positions = np.argwhere(self.grid == 0)
        return [tuple(pos) for pos in empty_positions]
    
    def move(self, direction: str) -> bool:
        """
        Move tiles in the specified direction.
        
        Args:
            direction: 'up', 'down', 'left', or 'right'
            
        Returns:
            True if a move was made, False otherwise
        """
        # Storing
        old_grid = self.grid.copy()
        
        # Store previous grid state
        self.previous_grid = old_grid
        
        # Reset merged values
        self.merged_values = []
        
        if direction == "up":
            self._move_up()
        elif direction == "down":
            self._move_down()
        elif direction == "left":
            self._move_left()
        elif direction == "right":
            self._move_right()
        else:
            logger.warning(f"Invalid direction: {direction}")
            return False
        
        # Check if board changed
        if not np.array_equal(old_grid, self.grid):
            self.move_count += 1
            self._add_random_tile()
            return True
        
        return False
    
    def _move_left(self):
        """Move tiles to the left"""
        for i in range(self.size):
            self.grid[i] = self._compress_and_merge(self.grid[i])
    
    def _move_right(self):
        """Move tiles to the right"""
        for i in range(self.size):
            self.grid[i] = self._compress_and_merge(self.grid[i][::-1])[::-1]
    
    def _move_up(self):
        """Move tiles up"""
        for j in range(self.size):
            column = self.grid[:, j].copy()
            self.grid[:, j] = self._compress_and_merge(column)
    
    def _move_down(self):
        """Move tiles down"""
        for j in range(self.size):
            column = self.grid[:, j].copy()
            self.grid[:, j] = self._compress_and_merge(column[::-1])[::-1]
    
    def _compress_and_merge(self, line: np.ndarray) -> np.ndarray:
        """
        Compress and merge a line.
        
        Args:
            line: A row or column of the board
            
        Returns:
            The processed line as numpy array
        """
        # Remove zeros
        non_zero = line[line != 0]
        
        # Merge adjacent equal values
        merged = []
        i = 0
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged_value = int(non_zero[i] * 2)
                self.merged_values.append(merged_value)
                merged.append(merged_value)
                self.score += merged_value
                i += 2
            else:
                merged.append(int(non_zero[i]))
                i += 1
        
        # Pad with zeros
        result = np.zeros(self.size, dtype=np.int32)
        result[:len(merged)] = merged
        return result
    
    def can_move(self, direction: str) -> bool:
        """Check if a move in the specified direction is possible"""
        test_board = Board(self.size)
        test_board.grid = self.grid.copy()
        moved = test_board.move(direction)
        return moved
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get valid neighbor positions for a given cell"""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.size and 0 <= c < self.size:
                neighbors.append((r, c))
        
        return neighbors
    
    def is_game_over(self) -> bool:
        """Check if the game is over (no more moves possible)"""
        # Check for empty cells
        if self._get_empty_cells():
            return False
        
        # Check for possible merges
        for i in range(self.size):
            for j in range(self.size):
                current = self.grid[i][j]
                # Check right
                if j + 1 < self.size and self.grid[i][j + 1] == current:
                    return False
                # Check down
                if i + 1 < self.size and self.grid[i + 1][j] == current:
                    return False
        return True
    
    def has_won(self) -> bool:
        """Check if the player has reached 2048"""
        return np.any(self.grid == 2048)
    
    def get_grid(self) -> List[List[int]]:
        """Get a copy of the current grid as list of lists"""
        return self.grid.astype(int).tolist()
    
    def reset(self):
        """Reset the board for a new game"""
        self.grid = np.zeros((self.size, self.size), dtype=np.int32)
        self.score = 0
        self.move_count = 0
        self._add_random_tile()
        self._add_random_tile()
        logger.info("Board reset")
        
    def get_previous_grid(self) -> Optional[List[List[int]]]:
        """Get the previous grid state as list of lists"""
        if self.previous_grid is not None:
            return self.previous_grid.astype(int).tolist()
        return None
    
    def grid_changed(self) -> bool:
        """Check if the grid has changed since the last move"""
        if self.previous_grid is None:
            return True
        return not np.array_equal(self.grid, self.previous_grid)
