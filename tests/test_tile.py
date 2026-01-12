"""Unit tests for the Tile class"""

import unittest
from src.game.tile import Tile

class TestTile(unittest.TestCase):
    """Test cases for the Tile class"""
    
    def test_tile_creation(self):
        """Test tile creation"""
        tile = Tile(value=2, row=0, col=0)
        self.assertEqual(tile.value, 2)
        self.assertEqual(tile.row, 0)
        self.assertEqual(tile.col, 0)
    
    def test_empty_tile(self):
        """Test empty tile detection"""
        empty = Tile(value=0)
        filled = Tile(value=2)
        self.assertTrue(empty.is_empty())
        self.assertFalse(filled.is_empty())
    
    def test_tile_equality(self):
        """Test tile equality comparison"""
        tile1 = Tile(value=4)
        tile2 = Tile(value=4)
        tile3 = Tile(value=2)
        self.assertEqual(tile1, tile2)
        self.assertNotEqual(tile1, tile3)

if __name__ == "__main__":
    unittest.main()
