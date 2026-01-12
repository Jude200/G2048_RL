"""Game manager handling game state and logic"""
import numpy as np


from typing import Optional
from src.utils.helpers import find_empty_cells
from src.utils.logger import get_logger
from .board import Board


logger = get_logger(__name__)

class GameManager:
    """Manages the overall game state and logic"""
    
    def __init__(self):
        """Initialize the game manager"""
        self.board = Board()
        self.is_game_over = False
        self.is_won = False
        self.best_score = 0
        logger.info("GameManager initialized")
    
    def start_new_game(self):
        """Start a new game"""
        if self.board.score > self.best_score:
            self.best_score = self.board.score
        
        self.board.reset()
        self.is_game_over = False
        self.is_won = False
        logger.info(f"New game started. Best score: {self.best_score}")
    
    def handle_move(self, direction: str) -> bool:
        """
        Handle a move in the specified direction.
        
        Args:
            direction: 'up', 'down', 'left', or 'right'
            
        Returns:
            True if move was successful, False otherwise
        """
        if self.is_game_over or self.is_won:
            logger.warning("Cannot move: game is over or won")
            return False
        
        moved = self.board.move(direction)
        
        if moved:
            # Check win condition
            if self.board.has_won():
                self.is_won = True
                logger.info("Player reached 2048!")
            
            # Check game over condition
            if self.board.is_game_over():
                self.is_game_over = True
                logger.info(f"Game Over! Final score: {self.board.score}")
        
        return moved
    
    def get_current_score(self) -> int:
        """Get the current game score"""
        return self.board.score
    
    def get_best_score(self) -> int:
        """Get the best score"""
        return self.best_score
    
    def get_board(self):
        """Get the current board grid"""
        return self.board.get_grid()
    
    def undo(self):
        """Undo the last move (if implemented)"""
        logger.info("Undo not yet implemented")
    
    def restart(self):
        """Restart the current game"""
        self.board.reset()
        self.is_game_over = False
        self.is_won = False
        logger.info("Game restarted")
    
    def step(self, action: str) -> tuple:
        """
        Execute one step in the game (RL environment style).
        
        Args:
            action: 'up', 'down', 'left', or 'right'
            
        Returns:
            tuple: (state, reward, done, info)
                - state: Current board state as list
                - reward: Reward from this action
                - done: Whether the game is over or won
                - info: Additional info (score, etc.)
        """
        # Make the move
        moved = self.handle_move(action)
        
        # Get current state
        state = self.get_board()
        
        # Calculate reward
        reward = self.reward() if moved else 0
        
        # Ending condition
        done = self.is_game_over or self.is_won
        
        # 
        return state, reward, done
    
    def get_valid_moves(self) -> list:
        """Get a list of valid moves from the current state"""
        valid_moves = []
        for direction in ['up', 'down', 'left', 'right']:
            valid_moves.append(self.board.can_move(direction))
        return valid_moves


    def reward(self):
        # Si le jeu est fini, grosse pénalité
        if self.is_game_over:
            return -10.0

        grid = self.board.grid
        reward = 0.0
        
        # 1. RÉCOMPENSE DE FUSION (Basée sur les tuiles fusionnées au dernier tour)
        # On utilise log2 pour ne pas écraser les autres récompenses avec des chiffres énormes
        if self.board.merged_values:
            reward += 0.1 * sum([np.log2(v) for v in self.board.merged_values])

        # 2. BONUS DE CASES VIDES
        # Plus il y a de vide, plus l'agent est récompensé (croissance non-linéaire)
        empty_cells = len(self.board._get_empty_cells())
        if empty_cells > 0:
            reward += 0.5 * empty_cells # Bonus constant par case vide

        # 3. MONOTONIE (Alignement des tuiles)
        # On vérifie si les valeurs augmentent ou diminuent de manière constante
        # monotonicity = 0
        # # Lignes
        # for i in range(4):
        #     row = grid[i, :]
        #     # On ne compte que les cases non vides pour la monotonie
        #     values = row[row != 0]
        #     if len(values) > 1:
        #         diffs = np.diff(np.log2(values))
        #         if np.all(diffs <= 0) or np.all(diffs >= 0): # Trié dans un sens
        #             monotonicity += sum(np.abs(diffs))
        # # Colonnes
        # for j in range(4):
        #     col = grid[:, j]
        #     values = col[col != 0]
        #     if len(values) > 1:
        #         diffs = np.diff(np.log2(values))
        #         if np.all(diffs <= 0) or np.all(diffs >= 0):
        #             monotonicity += sum(np.abs(diffs))
        
        # reward += 0.1 * monotonicity

        # # 4. MATRICE DE POIDS (Stratégie du coin)
        # # On veut inciter l'IA à mettre les grosses tuiles en haut à gauche
        # weights = np.array([
        #     [100, 50, 20, 10],
        #     [50,  20, 10,  5],
        #     [20,  10,  5,  2],
        #     [10,   5,  2,  1]
        # ])
        
        snake_weights =  np.log2(np.array([
            [65536, 32768, 16384, 8192],
            [512, 1024, 2048, 4096],
            [256, 128, 64, 32],
            [2, 4, 8, 16]
        ]))
        
        # On multiplie log2(tuile) par le poids de sa position
        weighted_sum = 0
        # np.sum(np.sum(np.log2(grid) * snake_weights, axis=0))
        for i in range(4):
            for j in range(4):
                if grid[i][j] > 0:
                    weighted_sum += np.log2(grid[i][j]) * snake_weights[i][j]
        
        reward += 0.01 * weighted_sum
        # print("Reward:", reward)
        return np.clip(reward, -10, 10)
    
    # def reward(self) -> int:
    #     """Calculate reward based on current board state"""
    #     # Monotonie
    #     # monotonity_reward = ...
        
    #     # Empty Cell Reward
    #     empty_reward = len(self.board._get_empty_cells())
        
    #     # Weighted
    #     weights = np.array([[65536, 32768, 16384, 8192],
    #                         [512, 1024, 2048, 4096],
    #                         [256, 128, 64, 32],
    #                         [2, 4, 8, 16]])
    #     fusion_reward = np.sum(np.log2(weights * (self.board.grid + 1)))
        
    #     # Smoothness 
    #     smoothness_reward = 0
    #     for i in range(self.board.size):
    #         for j in range(self.board.size):
    #             if self.board.grid[i][j] != 0:
    #                 value = np.log2(self.board.grid[i][j])
    #                 for neighbor in self.board.get_neighbors(i, j):
    #                     n_value = np.log2(self.board.grid[neighbor[0]][neighbor[1]]) if self.board.grid[neighbor[0]][neighbor[1]] != 0 else 0
    #                     smoothness_reward += abs(value - n_value)
        
    #     # End of game penalty
    #     end_penalty = -10 if self.is_game_over else 0
        
    #     # Total reward
    #     total_reward = int(0.1 * fusion_reward + 0.5 * empty_reward - 0.1 * smoothness_reward + end_penalty) / 16
    #     # print(f"Total Reward: {total_reward} | Fusion: {fusion_reward} | Empty: {empty_reward} | Smoothness: {smoothness_reward} | End Penalty: {end_penalty}")
    #     return total_reward * 2