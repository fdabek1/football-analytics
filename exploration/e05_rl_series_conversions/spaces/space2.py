from .space import Space
from collections import deque


class Space2(Space):
    def __init__(self, question, r_right, r_step):
        super(Space2, self).__init__(question, r_right, r_step)
        self.states = []
        self.history = deque(maxlen=5)
        self.build_states()

    def build_states(self):
        self.states.append('')
        for a1 in self.ACTIONS:
            self.states.append('|' + a1)
            for a2 in self.ACTIONS:
                self.states.append(a1 + '|' + a2)

    def get_state_string(self):
        if len(self.history) == 0:
            return ''
        elif len(self.history) == 1:
            return '|' + self.history[0]
        else:
            return self.history[0] + '|' + self.history[1]

    def reset(self):
        super(Space2, self).reset()
        self.history.clear()
        return self.states.index(self.get_state_string())

    def step(self, action):
        super(Space2, self).step(action)
        self.history.append(self.ACTIONS[action])
        done = self.is_goal()
        reward = 1 if done else 0
        return self.states.index(self.get_state_string()), reward, done

    def get_num_states(self):
        return len(self.states)
