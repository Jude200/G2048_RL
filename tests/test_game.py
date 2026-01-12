"""Unit tests for the GameManager class"""

import unittest
from src.game.game import GameManager

class TestGameManager(unittest.TestCase):
    """Test cases for the GameManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = GameManager()
    
    def test_initialization(self):
        """Test GameManager initialization"""
        self.assertIsNotNone(self.manager.board)
        self.assertFalse(self.manager.is_game_over)
        self.assertFalse(self.manager.is_won)
        self.assertEqual(self.manager.best_score, 0)
    
    def test_new_game(self):
        """Test starting a new game"""
        self.manager.board.score = 100
        self.manager.start_new_game()
        self.assertEqual(self.manager.best_score, 100)
        self.assertEqual(self.manager.board.score, 0)
    
    def test_handle_move(self):
        """Test handling moves"""
        initial_count = self.manager.board.move_count
        self.manager.board.grid = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.manager.handle_move("left")
        self.assertGreater(self.manager.board.move_count, initial_count)

if __name__ == "__main__":
    unittest.main()
