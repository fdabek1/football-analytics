class SampleSpace(object):
    ACTIONS = ['Bar', 'Line', 'AB', 'BA']
    STATES = ['NoneNone', 'NoneAB', 'NoneBA', 'BarNone', 'LineNone', 'BarAB', 'BarBA', 'LineAB', 'LineBA']

    def __init__(self, r_right=1, r_step=-1):
        self.r_right = r_right
        self.r_step = r_step

        self.viz = None
        self.var = None

    def step(self, action):
        action = self.ACTIONS[action]
        if action == 'Bar' or action == 'Line':
            self.viz = action
        elif action == 'AB' or action == 'BA':
            self.var = action

        done = self.is_goal()
        reward = self.r_right if done else self.r_step
        return self.STATES.index(self.get_state_string()), reward, done

    def reset(self):
        self.viz = None
        self.var = None
        return self.STATES.index(self.get_state_string())

    def get_state_string(self):
        return str(self.viz) + str(self.var)

    def get_num_actions(self):
        return len(self.ACTIONS)

    def get_num_states(self):
        return len(self.STATES)

    def is_goal(self):
        return self.viz == 'Bar' and self.var == 'BA'
