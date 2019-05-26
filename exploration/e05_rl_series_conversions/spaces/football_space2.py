from exploration.e05_rl_series_conversions.spaces.football_space import FootballSpace


class FootballSpace2(FootballSpace):
    ACTIONS = [
        {
            'title': 'turnover',
            'columns': ['fumble_lost', 'interception', 'safety'],
            'reward': -7,
        },
        {
            'title': 'scored',
            'columns': ['pass_touchdown', 'rush_touchdown'],
            'reward': 7,
        },
        {
            'title': 'first_down',
            'columns': ['first_down_rush', 'first_down_pass', 'first_down_penalty'],
            'reward': 3,
        },
        {
            'title': 'minor',
            'play_types': ['field_goal', 'punt'],
            'reward': -3,
        },
        {
            'title': 'useless',
            'play_types': ['qb_spike', 'qb_kneel'],
            'reward': 0,
        },
        {
            'title': 'penalty',
            'columns': ['penalty'],
            'reward': -1,
        },
        {
            'title': 'regular',
        }
    ]

    @classmethod
    def find_action(cls, play):
        if play['play_type'] in ['pass', 'run']:
            for a, action in enumerate(cls.ACTIONS):
                if action['title'] == 'regular':
                    return a

        return super().find_action(play)

    def get_reward(self, action, play):
        if action['title'] == 'regular':
            return play['yards_gained'] / 5

        return super().get_reward(action, play)
