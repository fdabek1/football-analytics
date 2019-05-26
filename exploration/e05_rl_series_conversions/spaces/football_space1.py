from exploration.e05_rl_series_conversions.spaces.football_space import FootballSpace


class FootballSpace1(FootballSpace):
    ACTIONS = [
        {
            'title': 'overall',
        }
    ]

    @classmethod
    def find_action(cls, play):
        return 0

    @staticmethod
    def get_reward(action, play):
        if play['safety'] == 1:
            return -2

        if play['interception'] == 1 or play['fumble_lost'] == 1:
            return -7

        if play['pass_touchdown'] == 1 or play['rush_touchdown'] == 1:
            return 7

        if play['first_down_rush'] == 1 or play['first_down_pass'] == 1 or play['first_down_penalty'] == 1:
            return 3

        if play['play_type'] == 'field_goal':
            return -1

        if play['play_type'] in ['qb_spike', 'qb_kneel']:
            return 0

        if play['play_type'] == 'no_play':
            return -1

        if play['play_type'] == 'pass':
            return play['yards_gained'] / 5

        if play['play_type'] == 'run':
            return play['yards_gained'] / 5

        if play['play_type'] == 'punt' and play['penalty'] == 1:
            return -1

        if play['play_type'] == 'punt':
            return -4

        raise ValueError('Unable to determine reward.', play)
