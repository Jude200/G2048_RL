"""Main entry point for the 2048 game"""

import customtkinter as ctk
from src.agent.agent import G2048Agent
from src.ui.gui import GameGUI
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Start the 2048 game"""
    logger.info("Initializing 2048 Game")
    
    # Create root window
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    
    # Create and run GUI
    gui = GameGUI(root, G2048Agent(is_training=False))
    gui.run()

if __name__ == "__main__":
    main()
