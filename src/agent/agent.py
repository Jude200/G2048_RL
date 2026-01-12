import random
from src.agent.ai import Q2048
from src.agent.buffer import G2048ReplayBuffer
from src.game.game import GameManager
from src.utils.helpers import convert_action_to_numeric, load_config, plot_loss_curve

config = load_config()

import torch

# Retrieve training configuration
training_config = config['training']


class G2048Agent:
    """Agent for playing 2048 game automatically"""
    
    def __init__(self, game_manager: GameManager = None, is_training: bool = True):
        
        # Determine device
        config_device = training_config.get('device', 'auto')
        if config_device == 'auto':
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
            elif torch.backends.mps.is_available():
                self.device = torch.device("mps")
            else:
                self.device = torch.device("cpu")
        else:
            self.device = torch.device(config_device)
        
        print(f"Using device: {self.device}")

        # Reference to the game manager
        self.game_manager = game_manager if game_manager else GameManager()
        
        # Initialize the AI model and move to device
        self.ai_model = Q2048().to(self.device)
        
        if not is_training:
            self.epsilon = training_config.get('epsilon_end', 0.05)   # No exploration during evaluation
            
            # Load pre-trained model weights
            self.load_model(training_config.get('model_save_path', "models/g2048_model.pth"))
        else :
            # Epsilon for exploration-exploitation trade-off
            self.epsilon = training_config.get('epsilon_start', 1.0)
        
    def select_move(self, game_manager: GameManager) -> str:
        actions = ['up', 'down', 'left', 'right']
        if random.random() < self.epsilon: 
            action = random.choice(actions)
            # Verify action is valid
            valid_moves = game_manager.get_valid_moves()
            while not valid_moves[actions.index(action)]:
                action = random.choice(actions)
            return action
        else :
            with torch.no_grad():
                board_tensor = torch.tensor(game_manager.get_board(), dtype=torch.float32, device=self.device)
                board_tensor = board_tensor.unsqueeze(0).unsqueeze(0)  # Add batch and channel dimensions
                
                # Get valid moves
                valid_moves = game_manager.get_valid_moves()
                
                # Get Q-values from the model
                q_values = self.ai_model(board_tensor)
                
                # Mask invalid moves
                for i in range(len(actions)):
                    if not valid_moves[i]:
                        q_values[0][i] = -1000.0
                
                # Select the action with the highest Q-value
                _, predicted_action = torch.max(q_values, dim=1)
                
                return actions[predicted_action.item()]
        
    def train_model(self):

        # Target network and move to device
        target_net = Q2048().to(self.device)
        
        # Copy weights from policy to target network
        target_net.load_state_dict(self.ai_model.state_dict())

        # Warm-up steps
        self.game_manager.restart()
        
        # Get initial state
        state = self.game_manager.get_board()
        
        # 
        replay_buffer_size = training_config.get('replay_buffer_size', 10000)
        
        # Min batch size before training starts
        b_min = training_config.get('b_min', 1000)
        
        # Replay buffer
        replay_buffer = G2048ReplayBuffer(capacity=replay_buffer_size)
        
        # Optimizer
        optimizer = torch.optim.Adam(self.ai_model.parameters(), lr=training_config.get('learning_rate', 0.001))
        
        while len(replay_buffer) < b_min:
            # Select action
            action = self.select_move(self.game_manager)
            
            # Take action
            next_state, reward,  done = self.game_manager.step(action)
            
            # Get valid moves for next state
            next_valid_moves = self.game_manager.get_valid_moves()
            
            # Store transition in replay buffer
            replay_buffer.add(state, action, reward, next_state, done, next_valid_moves)
            state = next_state
            if done:
                self.game_manager.restart()
                state = self.game_manager.get_board()
                
        # Training loop would go here
        episodes = training_config.get('episodes', 1000)
        
        # 
        target_update_freq = training_config.get('target_update_freq', 500)
        
        
        # Frequency training occurs
        train_freq = training_config.get('train_freq', 100)
        
        # Losses
        losses = []
        
        # 
        step_count = 0
        
        # loops
        for episode in range(episodes):
            
            print(f">>> Starting episode {episode + 1}/{episodes}")
            
            # Reset game
            self.game_manager.restart()
            
            # Get initial state
            state = self.game_manager.get_board()
            
            # Initialize done flag
            done = False
            
            while not done:
                # Select action
                action = self.select_move(self.game_manager)
                
                # Take action
                next_state, reward,  done = self.game_manager.step(action)
                
                # Get valid moves for next state
                next_valid_moves = self.game_manager.get_valid_moves()
                
                # Store transition in replay buffer
                replay_buffer.add(state, action, reward, next_state, done, next_valid_moves)
                
                state = next_state
                
                # Training
                if len(replay_buffer) > b_min and step_count % train_freq == 0:
                    batch = replay_buffer.sample(training_config.get('batch_size', 64))
                    
                    # Loss calculation and backpropagation would go here
                    loss = self.compute_loss(batch, target_net)
                    
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    # print(f"Episode {episode + 1}, Step {step_count}, Loss: {loss.item():.4f}")
                    losses.append(loss.item())
                
                # Update target network periodically
                if step_count > 0 and step_count % target_update_freq == 0:
                    target_net.load_state_dict(self.ai_model.state_dict())
                
                
                step_count += 1
            
            # Decay epsilon (exponential decay)
            self.epsilon = max(
                    training_config.get('epsilon_end', 0.05),
                    self.epsilon * training_config.get('epsilon_decay', 0.995)
                )

            if episode % training_config.get('checkpoint_freq', 10) == 0:
                self.save_model(training_config.get('model_save_path', 'g2048_model.pth'))

        self.save_model(training_config.get('model_save_path', 'g2048_model.pth'))
        plot_loss_curve(losses)
                
    def compute_loss(self, batch, target_net: Q2048) -> torch.Tensor:
        """Compute the loss for a batch of transitions"""
        
        states, actions, rewards, next_states, dones, next_valid_moves = batch
        
        # Convert to tensors on the correct device
        state_batch = torch.tensor(states, dtype=torch.float32, device=self.device)
        state_batch = state_batch.unsqueeze(1)  # Add channel dimension
        
        # 
        q_values = self.ai_model(state_batch)
        
        # 
        actions_numeric = convert_action_to_numeric(actions)  # Convertit ['left', 'right', ...] 
        
        q_sa = q_values.gather(1, torch.tensor(actions_numeric, dtype=torch.long, device=self.device).unsqueeze(1)).squeeze(1)
        
        with torch.no_grad():
            next_q = target_net(torch.tensor(next_states, dtype=torch.float32, device=self.device).unsqueeze(1))
            
            # Mask invalid moves in next states to avoid overestimation
            # We need valid moves for each state in the batch
            next_valid_moves_tensor = torch.tensor(next_valid_moves, dtype=torch.bool, device=self.device)
            next_q[next_valid_moves_tensor == False] = -1000.0  # Masking manually to be safe with different torch versions

            max_next_q = next_q.max(1)[0]
            
            target = torch.tensor(rewards, dtype=torch.float32, device=self.device) + \
                     training_config.get('gamma', 0.99) * max_next_q * (1 - torch.tensor(dones, dtype=torch.float32, device=self.device))
        
        # Use Huber Loss (SmoothL1Loss) which is more robust to outliers than MSE
        loss_fn = torch.nn.MSELoss()
        loss = loss_fn(q_sa, target)
        return loss
        
    def save_model(self, filepath: str):
        """Save the model weights to a file."""
        torch.save(self.ai_model.state_dict(), filepath)
        print(f"Model saved to {filepath}")

        def load_model(self, filepath: str):

            """Load the model weights from a file."""

            try:

                self.ai_model.load_state_dict(torch.load(filepath, map_location=self.device))

                self.ai_model.eval()

                print(f"Model loaded from {filepath} onto {self.device}")

            except FileNotFoundError:

                print(f"Error: Model file not found at {filepath}")

            except Exception as e:

                print(f"Error loading model: {e}")

    