import torch 
import torch.nn as nn

class Q2048(nn.Module):
    """AI agent for playing 2048 game"""
    
    def __init__(self, num_actions: int = 4):
      
        super(Q2048, self).__init__()
        
        # Convolutional layers to process the board state
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=64, kernel_size=2, padding=1)
        
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=2, padding=1)
        
        # Fully connected layers to decide the best move
        self.fc1 = nn.Linear(128 * 6 * 6, 256)
        
        self.fc2 = nn.Linear(256, num_actions)
        
        
    def forward(self, state: torch.Tensor) -> torch.Tensor:
        """Forward pass to predict the best move"""
        
        # Apply log2 transformation and normalize to [0, 1]
        state = torch.log2(state + 1) / 16 # 17 = log2(131072 + 1) max possible tile
        
        # Conv block 1
        x = torch.relu(self.conv1(state))
        
        # Conv block 2
        x = torch.relu(self.conv2(x))
        
        # Flatten the output
        x = x.view(x.size(0), -1)
        
        # FC block 1
        x = torch.relu(self.fc1(x))
        
        return self.fc2(x)
    

