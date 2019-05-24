from .space import Space
import json


class Space1(Space):
    def __init__(self, question, r_right, r_step):
        self.states = []
        self.build_states()
        self.goal = self.MAP_TABS[1] + '|' + self.LOCATIONS[3] + '|' + self.Y_VALUES[0] + '|' + self.CHARTS[
            1] + '|' + self.YEARS[2]

        super(Space1, self).__init__(question, r_right, r_step)

    def build_states(self):
        for tab in self.MAP_TABS:
            for location in self.LOCATIONS:
                for y in self.Y_VALUES:
                    for chart in self.CHARTS:
                        for year in self.YEARS:
                            current = tab + '|' + location + '|' + y + '|' + chart + '|' + year
                            self.states.append(current)

    def get_state_string(self):
        return self.tab + '|' + self.location + '|' + self.y + '|' + self.chart + '|' + self.year

    def reset(self):
        super(Space1, self).reset()
        return self.states.index(self.get_state_string())

    def step(self, action):
        super(Space1, self).step(action)
        done = self.is_goal()
        reward = self.r_right if done else self.r_step
        return self.states.index(self.get_state_string()), reward, done

    def get_num_states(self):
        return len(self.states)

    def save_constants(self):
        data = {
            'states': self.states,
            'actions': [self.MAP_TABS, self.LOCATIONS, self.Y_VALUES, self.CHARTS, self.YEARS]
        }

        with open('../api/app/Learning/Tables/constants.json', 'wb') as w:
            json.dump(data, w)
        exit()
