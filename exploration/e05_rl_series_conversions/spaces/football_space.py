class FootballSpace:
    STATES = []
    ACTIONS = [
        {
            'title': 'fumble_lost',
            'columns': ['fumble_lost'],
            'reward': -7,
        },
        {
            'title': 'touchdown',
            'columns': ['pass_touchdown', 'rush_touchdown'],
            'reward': 7,
        },
        {
            'title': 'first_down',
            'columns': ['first_down_rush', 'first_down_pass', 'first_down_penalty'],
            'reward': 3,
        },
        {
            'title': 'interception',
            'columns': ['interception'],
            'reward': -7,
        },
        {
            'title': 'safety',
            'columns': ['safety'],
            'reward': -2,
        },
        {
            'title': 'field_goal',
            'play_types': ['field_goal'],
            'reward': -1,
        },
        {
            'title': 'punt',
            'play_types': ['punt'],
            'reward': -3,
        },
        {
            'title': 'regular',  # This needs to be last to be last one evaluated
            'play_types': ['qb_spike', 'qb_kneel', 'pass', 'run'],
            'reward': 0,
        },
        {
            'title': 'penalty',
            'columns': ['penalty'],
            'reward': 0,
        },
    ]

    @classmethod
    def populate_states(cls):
        for down in [1, 2, 3, 4]:
            for distance in range(1, 50):
                cls.STATES.append(str(down) + '|' + str(distance))

        cls.STATES.append('success')
        cls.STATES.append('fail')

    @classmethod
    def find_action(cls, play):
        for i, action in enumerate(cls.ACTIONS):
            if 'play_types' in action:
                if play['play_type'] in action['play_types'] and play['penalty'] == 0:
                    return i
            elif 'columns' in action:
                for col in action['columns']:
                    if play[col] > 0:
                        return i
            elif play[action['type']] > 0:
                return i

        raise ValueError('Unable to find action for this play:', play)

    @classmethod
    def find_state(cls, index):
        return cls.STATES[index]

    def __init__(self):
        self.down = None
        self.distance = None
        self.success = None

    def get_num_actions(self):
        return len(self.ACTIONS)

    def get_num_states(self):
        return len(self.STATES)

    @staticmethod
    def get_reward(action, play):
        if 'reward' in action:
            return action['reward']

        raise ValueError('Unable to identify reward.')

    def step(self, a, play, next_down, next_distance):
        if next_distance is None:
            self.success = next_down
        else:
            self.down = next_down
            self.distance = next_distance

        reward = self.get_reward(self.ACTIONS[a], play)
        return self.get_state(), reward, False

    def get_state_string(self):
        if self.success is not None:
            return 'success' if self.success else 'fail'

        return str(self.down) + '|' + str(self.distance)

    def get_state(self):
        return self.STATES.index(self.get_state_string())

    def reset(self):
        self.down = 1
        self.distance = 10
        self.success = None

        return self.get_state()
