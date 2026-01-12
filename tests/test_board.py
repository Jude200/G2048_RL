"""Unit tests for the Board class"""

import unittest
import numpy as np
from src.game.board import Board

class TestBoard(unittest.TestCase):
    """Test cases for the Board class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.board = Board()
    
    def test_board_initialization(self):
        """Test that board initializes correctly"""
        self.assertEqual(self.board.size, 4)
        self.assertEqual(self.board.score, 0)
        self.assertEqual(self.board.move_count, 0)
    
    def test_board_has_tiles(self):
        """Test that board starts with 2 tiles"""
        non_zero_count = np.count_nonzero(self.board.grid)
        self.assertEqual(non_zero_count, 2)
    
    def test_move_left(self):
        """Test moving tiles left"""
        self.board.grid = np.array([
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], dtype=np.int32)
        self.board.move("left")
        self.assertEqual(self.board.grid[0][0], 4)
    
    def test_move_right(self):
        """Test moving tiles right"""
        self.board.grid = np.array([
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], dtype=np.int32)
        self.board.move("right")
        self.assertEqual(self.board.grid[0][3], 4)
    
    def test_game_over_detection(self):
        """Test game over detection"""
        # Fill board with non-mergeable tiles
        self.board.grid = np.array([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ], dtype=np.int32)
        self.assertTrue(self.board.is_game_over())
    
    def test_empty_cells_detection(self):
        """Test detection of empty cells"""
        self.board.grid = np.array([
            [2, 0, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ], dtype=np.int32)
        self.assertFalse(self.board.is_game_over())

if __name__ == "__main__":
    unittest.main()
