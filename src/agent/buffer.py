import random
from collections import deque

class G2048ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done, next_valid_moves):
        self.buffer.append((state, action, reward, next_state, done, next_valid_moves))
        

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones, next_valid_moves = zip(*batch)
        return states, actions, rewards, next_states, dones, next_valid_moves

    def __len__(self):
        return len(self.buffer)
