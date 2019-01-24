import numpy as np
from os.path import isfile

# get help from:
# https://medium.com/@yvanscher/making-a-game-ai-with-deep-learning-963bb549b3d5

class QTable:
    
    #def __init__(self, objectives, actions, alpha=0.1, reward_decay = 0.9, eps = 0.7):
    #    self._objectives = objectives
    def __init__(self, actions, alpha=0.1, reward_decay = 0.9, eps = 0.7):
        self._actions = actions
        self._alpha = alpha
        self._reward_decay = reward_decay
        self._eps = eps
        self._states = set()
        self._qtable = self._load("qtable") if isfile("qtable") else np.zeros((0, len(self._actions)))

    def _load(self, fname):return np.load(fname)

    """def getAvailableActions(self, state):
        result = []
        for i, obj_key in enumerate(self._objectives):
            if self._objectives[obj_key] > state[i]:result.append(obj_key)
        return result"""

    def get_action(self, state):
        selected_action = None
        if np.random.rand() < (1 - self._eps):
            selected_action = np.random.randint(0, len(self._actions))
        else:
            if state not in self._states:
                self.add_state(state)
            idx = list(self._states).index(state)
            q_values = self._qtable[idx]
            selected_action = int(np.argmax(q_values))
        return selected_action

    def add_state(self, state):
        self._qtable = np.vstack([self._qtable, np.zeros((1, len(self._actions)))])
        self._states.add(state)

    def update_qtable(self, state, next_state, action, reward):
        if state not in self._states:self.add_state(state)
        if next_state not in self._states:self.add_state(next_state)

        state_idx = list(self._states).index(state)
        next_state_idx = list(self._states).index(next_state)
        q_state = self._qtable[state_idx, action]
        q_next_state = self._qtable[next_state_idx].max()
        q_targets = reward + (self._reward_decay * q_next_state)
        loss = q_targets - q_state
        self._qtable[state_idx, action] += self._alpha * loss
        return loss

    def save(self):
        np.save("qtable", self._qtable)