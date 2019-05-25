from gym import Env, spaces
from exploration.e05_rl_series_conversions.spaces.space import FootballSpace


class DashboardEnv(Env):
    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, space):
        FootballSpace.populate_states()
        self.space = FootballSpace()
        self.action_space = spaces.Discrete(self.space.get_num_actions())
        self.observation_space = spaces.Discrete(self.space.get_num_states())
        self.state = None

    def step(self, data):
        a, next_down, next_distance = data
        s, r, d = self.space.step(a, next_down, next_distance)
        self.state = s
        return s, r, d, {}

    def reset(self):
        self.state = self.space.reset()
        return self.state

    def render(self, mode='human'):
        pass

    # def render(self, mode='human', close=False):
    #     if close:
    #         return
    #
    #     outfile = StringIO() if mode == 'ansi' else sys.stdout
    #
    #     row, col = self.s // self.ncol, self.s % self.ncol
    #     desc = self.desc.tolist()
    #     desc = [[c.decode('utf-8') for c in line] for line in desc]
    #     desc[row][col] = utils.colorize(desc[row][col], "red", highlight=True)
    #     outfile.write("\n".join(''.join(line) for line in desc) + "\n")
    #     if self.last_action is not None:
    #         outfile.write("  ({})\n".format(["Left", "Down", "Right", "Up"][self.last_action]))
    #     else:
    #         outfile.write("\n")
    #
    #     return outfile
