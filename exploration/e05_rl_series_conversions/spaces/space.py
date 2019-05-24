from ..questions import Question


class Space(object):
    ACTIONS = []
    # Configs
    MAP_TABS = ['regions', 'states']
    LOCATIONS = ['USA',
                 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
                 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
                 'Pacific', 'Mountain', 'West North Central', 'West South Central',
                 'East North Central', 'East South Central',
                 'Middle Atlantic', 'South Atlantic', 'New England']
    Y_VALUES = ['avg_services', 'avg_unique_benes', 'avg_submitted_chrg_amt', 'avg_medicare_allowed_amt',
                'avg_medicare_payment_amt']
    CHARTS = ['barGender', 'barAge', 'barRace']
    YEARS = ['2014', '2013', '2012']

    def __init__(self, question, r_right=1, r_step=-1):
        self.r_right = r_right
        self.r_step = r_step

        self.tab = None
        self.location = None
        self.y = None
        self.chart = None
        self.year = None
        self.question = Question(question)
        self.build_actions()

    def step(self, action):
        action = self.ACTIONS[action]
        if action in self.MAP_TABS:
            self.tab = action
        elif action in self.LOCATIONS:
            if action != 'USA':
                if len(action) == 2 and self.tab == 'states':
                    self.location = action
                elif len(action) > 2 and self.tab == 'regions':
                    self.location = action
        elif action in self.Y_VALUES:
            self.y = action
        elif action in self.CHARTS:
            self.chart = action
        elif action in self.YEARS:
            self.year = action
        elif action in self.LOCATIONS:
            self.location = action

    def reset(self):
        self.tab = self.MAP_TABS[0]
        self.location = self.LOCATIONS[0]
        self.y = self.Y_VALUES[0]
        self.chart = self.CHARTS[0]
        self.year = self.YEARS[0]

    def build_actions(self):
        for tab in self.MAP_TABS:
            self.ACTIONS.append(tab)

        for location in self.LOCATIONS:
            self.ACTIONS.append(location)

        for y in self.Y_VALUES:
            self.ACTIONS.append(y)

        for chart in self.CHARTS:
            self.ACTIONS.append(chart)

        for year in self.YEARS:
            self.ACTIONS.append(year)

    def get_num_actions(self):
        return len(self.MAP_TABS) + len(self.LOCATIONS) + len(self.Y_VALUES) + len(self.CHARTS) + len(self.YEARS)

    def get_num_states(self):
        return -1

    def is_goal(self):
        return self.question.is_goal(self)
