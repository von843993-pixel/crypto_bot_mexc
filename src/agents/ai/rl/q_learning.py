"""
═══════════════════════════════════════════════════════════════
Q-Learning Agent - Reinforcement learning for trading
═══════════════════════════════════════════════════════════════
"""
import numpy as np
from typing import Dict, Tuple, Any

class QLearningAgent:
    """Simple Q-Learning agent for trading"""
    
    def __init__(
        self,
        learning_rate: float = 0.1,
        discount_factor: float = 0.95,
        epsilon: float = 0.1,
    ):
        """Initialize Q-Learning agent"""
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        
        # Q-table: state -> action values
        self.q_table = {}
        
        # Actions: 0=HOLD, 1=BUY, 2=SELL
        self.actions = [0, 1, 2]
    
    def get_action(self, state: str) -> int:
        """Choose action (epsilon-greedy)"""
        if np.random.random() < self.epsilon:
            # Explore
            return np.random.choice(self.actions)
        else:
            # Exploit
            if state not in self.q_table:
                return 0  # Default to HOLD
            
            values = self.q_table[state]
            return np.argmax(values)
    
    def update(
        self,
        state: str,
        action: int,
        reward: float,
        next_state: str,
    ):
        """Update Q-values"""
        
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))
        
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(self.actions))
        
        # Q-learning update rule
        old_value = self.q_table[state][action]
        next_max = np.max(self.q_table[next_state])
        
        new_value = old_value + self.learning_rate * (
            reward + self.discount_factor * next_max - old_value
        )
        
        self.q_table[state][action] = new_value
    
    def discretize_state(
        self,
        rsi: float,
        macd_signal: float,
        bb_percent: float,
    ) -> str:
        """Convert continuous state to discrete"""
        
        rsi_bin = "RSI_LOW" if rsi < 40 else "RSI_MID" if rsi < 60 else "RSI_HIGH"
        macd_bin = "MACD_NEG" if macd_signal < 0 else "MACD_POS"
        bb_bin = "BB_LOW" if bb_percent < 30 else "BB_MID" if bb_percent < 70 else "BB_HIGH"
        
        return f"{rsi_bin}_{macd_bin}_{bb_bin}"
