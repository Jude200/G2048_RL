"""Main GUI for the 2048 game using customtkinter"""

import customtkinter as ctk
from typing import Callable, Optional
from src.agent.agent import G2048Agent
from src.game.game import GameManager
from src.utils.logger import get_logger
from .styles import (BG_COLOR, WINDOW_TITLE, TITLE_FONT, BUTTON_FONT, 
                     TEXT_PRIMARY, TEXT_SECONDARY, BUTTON_COLOR, BUTTON_HOVER_COLOR,
                     HEADER_COLOR, INFO_FONT, SUBTITLE_FONT, ACCENT_COLOR)
from .widgets import BoardWidget, ScoreDisplay

logger = get_logger(__name__)

class GameGUI:
    """Main GUI class for the 2048 game"""
    
    def __init__(self, root: Optional[ctk.CTk] = None, agent : G2048Agent = None):
        """
        Initialize the GUI.
        
        Args:
            root: Optional root window. If None, a new one is created.
        """
        self.root = root or ctk.CTk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry("460x700")
        self.root.configure(fg_color=BG_COLOR)
        self.root.resizable(False, False)
        
        self.agent = agent
        self.agent_play_mode = True if agent else False
        self.game_manager = GameManager()
        self._setup_ui()
        self._bind_keys()
        
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Header section
        self._create_header(main_frame)
        
        # Score display section
        self._create_score_section(main_frame)
        
        # Game board section
        self._create_board_section(main_frame)
        
        # Control buttons section
        self._create_controls_section(main_frame)
        
        # Info section
        self._create_info_section(main_frame)
    
    def _create_header(self, parent):
        """Create header with title"""
        header_frame = ctk.CTkFrame(parent, fg_color=HEADER_COLOR, corner_radius=12, height=80)
        header_frame.pack(fill="x", pady=(0, 16))
        header_frame.pack_propagate(False)
        
        title_container = ctk.CTkFrame(header_frame, fg_color=HEADER_COLOR)
        title_container.pack(fill="both", expand=True, padx=20, pady=16)
        
        title = ctk.CTkLabel(title_container, text="2048", font=TITLE_FONT, text_color=ACCENT_COLOR)
        title.pack(side="left")
        
        subtitle = ctk.CTkLabel(title_container, text="Reach the 2048 tile!", 
                               font=SUBTITLE_FONT, text_color=TEXT_SECONDARY)
        subtitle.pack(side="left", padx=(16, 0))
    
    def _create_score_section(self, parent):
        """Create score display section"""
        score_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR)
        score_frame.pack(fill="x", pady=(0, 12))
        
        self.score_display = ScoreDisplay(score_frame, width=420, height=60)
        self.score_display.pack_propagate(False)
        self.score_display.pack()
    
    def _create_board_section(self, parent):
        """Create game board section"""
        board_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR)
        board_frame.pack(fill="both", expand=True, pady=(0, 16))
        
        self.board_widget = BoardWidget(board_frame, size=4)
        self.board_widget.pack()
    
    def _create_controls_section(self, parent):
        """Create control buttons section"""
        button_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR)
        button_frame.pack(fill="x", pady=(0, 12))
        
        # New Game button (prominent)
        new_game_btn = ctk.CTkButton(
            button_frame,
            text="✨ New Game",
            font=BUTTON_FONT,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color="#000000",
            command=self.new_game,
            height=48,
            corner_radius=8
        )
        new_game_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        # Undo button
        undo_btn = ctk.CTkButton(
            button_frame,
            text="↶ Undo",
            font=BUTTON_FONT,
            fg_color="#404040",
            hover_color="#505050",
            command=self.undo,
            height=48,
            corner_radius=8
        )
        undo_btn.pack(side="left", padx=(8, 0), fill="x", expand=True)
    
    def _create_info_section(self, parent):
        """Create info section"""
        info_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR)
        info_frame.pack(fill="x")
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="↑ ↓ ← → or WASD to move",
            font=INFO_FONT,
            text_color=TEXT_SECONDARY
        )
        info_text.pack()
        
    def agent_play(self):
        """Play automatically using the agent"""
        if not self.agent or not self.agent_play_mode:
            return
        
        # Check if game is over
        if self.game_manager.is_game_over:
            self._show_message("Game Over!", f"Final score: {self.game_manager.get_current_score()}")
            self.agent_play_mode = False
            return
        
        if self.game_manager.is_won:
            self._show_message("🎉 Agent Won!", "Agent reached 2048!")
            self.agent_play_mode = False
            return
        
        # Get the agent's move
        move = self.agent.select_move(self.game_manager)
        
        # print(self.game_manager.board.grid_changed)
        
        # Execute the move
        self.game_manager.handle_move(move)
        self._update_display()
        
        # Continue playing - schedule next move
        self.root.after(500, self.agent_play)
        
        logger.info(f"Agent played move: {move}")
    
    def _bind_keys(self):
        """Bind keyboard controls"""
        self.root.bind("<Up>", lambda e: self._handle_key("up"))
        self.root.bind("<Down>", lambda e: self._handle_key("down"))
        self.root.bind("<Left>", lambda e: self._handle_key("left"))
        self.root.bind("<Right>", lambda e: self._handle_key("right"))
        self.root.bind("<w>", lambda e: self._handle_key("up"))
        self.root.bind("<s>", lambda e: self._handle_key("down"))
        self.root.bind("<a>", lambda e: self._handle_key("left"))
        self.root.bind("<d>", lambda e: self._handle_key("right"))
        self.root.bind("<W>", lambda e: self._handle_key("up"))
        self.root.bind("<S>", lambda e: self._handle_key("down"))
        self.root.bind("<A>", lambda e: self._handle_key("left"))
        self.root.bind("<D>", lambda e: self._handle_key("right"))
    
    def _handle_key(self, direction: str):
        """Handle keyboard input"""
        if self.game_manager.handle_move(direction):
            self._update_display()
            
            if self.game_manager.is_won:
                self._show_message("🎉 Congratulations!", "You reached 2048!\n\nWant to continue playing?")
            elif self.game_manager.is_game_over:
                self._show_message("Game Over!", f"Final score: {self.game_manager.get_current_score()}")
    
    def _update_display(self):
        """Update the display after a move"""
        self.board_widget.update_board(self.game_manager.get_board())
        self.score_display.update_score(
            self.game_manager.get_current_score(),
            self.game_manager.get_best_score()
        )
    
    def new_game(self):
        """Start a new game"""
        self.game_manager.start_new_game()
        self._update_display()
        logger.info("New game started")
    
    def undo(self):
        """Undo the last move"""
        self.game_manager.undo()
    
    def _show_message(self, title: str, message: str):
        """Show a message dialog"""
        try:
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(title=title, message=message, icon="info")
        except Exception as e:
            logger.warning(f"Could not show message box: {e}")
    
    def run(self):
        """Start the GUI"""
        self._update_display()
        logger.info("Starting GUI")
        # Start agent if enabled
        if self.agent_play_mode:
            self.root.after(250, self.agent_play)
        self.root.mainloop()
