"""Save and load game state"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SaveManager:
    """Manages game saves and loads"""
    
    def __init__(self, save_dir: str = "saves"):
        """
        Initialize the save manager.
        
        Args:
            save_dir: Directory to store save files
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
    
    def save_game(self, game_state: Dict, filename: str = "autosave.json") -> bool:
        """
        Save the current game state.
        
        Args:
            game_state: Dictionary containing game data
            filename: Name of the save file
            
        Returns:
            True if save was successful, False otherwise
        """
        try:
            filepath = self.save_dir / filename
            with open(filepath, 'w') as f:
                json.dump(game_state, f, indent=2)
            logger.info(f"Game saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            return False
    
    def load_game(self, filename: str = "autosave.json") -> Optional[Dict]:
        """
        Load a saved game.
        
        Args:
            filename: Name of the save file
            
        Returns:
            Dictionary containing game data, or None if load failed
        """
        try:
            filepath = self.save_dir / filename
            if not filepath.exists():
                logger.warning(f"Save file not found: {filepath}")
                return None
            
            with open(filepath, 'r') as f:
                game_state = json.load(f)
            logger.info(f"Game loaded from {filepath}")
            return game_state
        except Exception as e:
            logger.error(f"Failed to load game: {e}")
            return None
    
    def get_save_files(self) -> list:
        """Get list of all save files"""
        return [f.name for f in self.save_dir.glob("*.json")]
    
    def delete_save(self, filename: str) -> bool:
        """Delete a save file"""
        try:
            filepath = self.save_dir / filename
            filepath.unlink()
            logger.info(f"Save file deleted: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete save: {e}")
            return False
