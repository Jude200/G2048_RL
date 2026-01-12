import torch 
import torch.nn as nn

# class Q2048(nn.Module):
#     def __init__(self, input_dim=16, output_dim=4):
#         super().__init__()
#         self.fc1 = nn.Linear(input_dim, 512)
#         self.fc2 = nn.Linear(512, 512)
#         self.fc3 = nn.Linear(512, 128)
#         self.fc4 = nn.Linear(128, 128)
#         self.fc5 = nn.Linear(128, 128)
#         self.fc6 = nn.Linear(128, output_dim)

#     def forward(self, state: torch.Tensor) -> torch.Tensor :
#         # Apply log2 transformation and normalize to [0, 1]
#         state = torch.log2(state + 1) / 15.0  #
        
#         x = state.view(state.size(0), -1)  # Flatten the input
        
        
#         x = torch.relu(self.fc1(x))
#         x = torch.relu(self.fc2(x))
#         x = torch.relu(self.fc3(x))
#         x = torch.relu(self.fc4(x))
#         x = torch.relu(self.fc5(x))
#         return torch.softmax(self.fc6(x), dim=-1)

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
        state = torch.log2(state + 1) # 17 = log2(131072 + 1) max possible tile
        
        # Conv block 1
        x = torch.relu(self.conv1(state))
        
        # Conv block 2
        x = torch.relu(self.conv2(x))
        
        # Flatten the output
        x = x.view(x.size(0), -1)
        
        # FC block 1
        x = torch.relu(self.fc1(x))
        
        return self.fc2(x)
    

