"""Helper functions for the 2048 game"""
import yaml

import logging
import numpy as np
from typing import List, Tuple, Union


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure logging for the application"""
    logger = logging.getLogger("2048")
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def find_empty_cells(board: Union[np.ndarray, List[List[int]]]) -> List[Tuple[int, int]]:
    """Find all empty cells (value 0) in the board"""
    if isinstance(board, np.ndarray):
        empty_positions = np.argwhere(board == 0)
        return [tuple(pos) for pos in empty_positions]
    else:
        empty = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    empty.append((i, j))
        return empty

def is_valid_move(board: Union[np.ndarray, List[List[int]]]) -> bool:
    """Check if any move is possible"""
    # Check for empty cells
    if find_empty_cells(board):
        return True
    
    # Check for mergeable tiles
    if isinstance(board, np.ndarray):
        size = board.shape[0]
        for i in range(size):
            for j in range(size):
                current = board[i][j]
                # Check right
                if j + 1 < size and board[i][j + 1] == current:
                    return True
                # Check down
                if i + 1 < size and board[i + 1][j] == current:
                    return True
    else:
        size = len(board)
        for i in range(size):
            for j in range(size):
                current = board[i][j]
                # Check right
                if j + 1 < size and board[i][j + 1] == current:
                    return True
                # Check down
                if i + 1 < size and board[i + 1][j] == current:
                    return True
    
    return False

def load_config(config_path: str = 'config/config.yaml'):
    """Loads configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        return None
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None
    
def convert_action_to_numeric(action: List[str]) -> List[int]:
    """Convert action list from strings to numeric representation"""
    action_map = {'up': 0, 'down': 1, 'left': 2, 'right': 3}
    return [action_map[a] for a in action if a in action_map]

def plot_loss_curve(losses: List[float], save_path: str = 'figures/loss_curve.png'):
    """Plot and save the loss curve"""
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 5))
    plt.plot(losses, label='Loss')
    plt.xlabel('Training Steps')
    plt.ylabel('Loss')
    plt.title('Training Loss Curve')
    plt.legend()
    plt.grid()
    plt.savefig(save_path)
    plt.close()