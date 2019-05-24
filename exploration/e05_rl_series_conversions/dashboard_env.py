import sys

from gym import Env, spaces, utils
from six import StringIO  # TODO - Maybe dont use this

# from .football_space import FootballSpace
# from .spaces.space1 import Space1
# from .spaces.space2 import Space2
# from .spaces.sample import SampleSpace


# State spaces:
# -Have every possible configuration of the dashboard.  Compare to when the correct dashboard config exists
# -Last action

class DashboardEnv(Env):
    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self):
        self.last_action = None  # for rendering
        self.nA = self.space.get_num_actions()
        self.nS = self.space.get_num_states()

        self.action_space = spaces.Discrete(self.nA)
        self.observation_space = spaces.Discrete(self.nS)

    def step(self, action):
        s, r, d = self.space.step(action)
        self.s = s
        self.last_action = action
        return s, r, d, {}

    def reset(self):
        self.s = self.space.reset()
        return self.s

    def render(self, mode='human', close=False):
        if close:
            return

        outfile = StringIO() if mode == 'ansi' else sys.stdout

        row, col = self.s // self.ncol, self.s % self.ncol
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        desc[row][col] = utils.colorize(desc[row][col], "red", highlight=True)
        outfile.write("\n".join(''.join(line) for line in desc) + "\n")
        if self.last_action is not None:
            outfile.write("  ({})\n".format(["Left", "Down", "Right", "Up"][self.last_action]))
        else:
            outfile.write("\n")

        return outfile
