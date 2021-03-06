import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import gym
import os


class Learner:
    def __init__(self, save_files=False, show_graphs=True, verbose=True):
        self.save_files = save_files
        self.show_graphs = show_graphs
        self.verbose = verbose
        self.df = None
        self.__load_series()

    def __load_series(self):
        if os.path.exists('series.csv'):
            self.df = pd.read_csv('series.csv')
            return

        df = pd.read_csv('../../data/reg_pbp_2018_CarMel_RmvCol_for_firstdown_success.csv')
        max_yds_to_go = df['ydstogo'].max()

        df = df[df['play_type'].isin(
            ['no_play', 'pass', 'punt', 'run', 'field_goal', 'qb_kneel', 'qb_spike'])
        ]

        df = df[df['down'].notnull()]
        df['down'] = df['down'].astype(int)
        df = df.reset_index(drop=True)

        df['series_num'] = -1
        df['series_success'] = False
        df['series_delete'] = False

        begin_series_index = 0
        series_num = 1

        # Go through dataframe by rows
        for index, row in df.iterrows():
            if row['game_id'] != df.iloc[index - 1]['game_id'] or (row['qtr'] == 3 and df.iloc[index - 1]['qtr'] == 2):
                if df.iloc[index - 1]['series_num'] == -1:
                    # df.loc[begin_series_index:index - 1, 'series_num'] = series_num
                    # df.loc[begin_series_index:index - 1, 'series_success'] = False
                    df.loc[begin_series_index:index - 1, 'series_delete'] = True
                    # print('delete', df.loc[begin_series_index:index - 1][['qtr', 'time']])
                    begin_series_index = index
                    # series_num += 1

            # Success
            if row['first_down_rush'] == 1 or row['first_down_pass'] == 1 or row['first_down_penalty'] == 1 \
                    or row['touchdown'] == 1:
                df.loc[begin_series_index:index, 'series_num'] = series_num
                df.loc[begin_series_index:index, 'series_success'] = True
                # print('success', df.loc[begin_series_index:index][['qtr', 'time']])
                begin_series_index = index + 1
                series_num += 1

            # Fail
            elif row['fourth_down_failed'] == 1 or row['interception'] == 1 or row['safety'] == 1 or \
                    row['fumble_lost'] == 1 or (row['play_type'] == 'punt' and row['penalty'] == 0) or \
                    row['play_type'] == 'field_goal':
                df.loc[begin_series_index:index, 'series_num'] = series_num
                df.loc[begin_series_index:index, 'series_success'] = False
                # print('fail', df.loc[begin_series_index:index][['qtr', 'time']])
                begin_series_index = index + 1
                series_num += 1

        # Delete end of half and end of game series
        df = df[~df['series_delete']]

        # Capture rows at the very end that could have been failures
        # print('after', df.loc[df['series_num'] == -1][['qtr', 'time']])
        df.loc[df['series_num'] == -1, 'series_success'] = False
        df.loc[df['series_num'] == -1, 'series_num'] = series_num

        self.df = df
        self.df.to_csv('series.csv', index=False)

    @staticmethod
    def get_next_down_distance(series, current_index):
        next_index = current_index + 1
        if next_index >= len(series):
            return series.iloc[0]['series_success'], None

        next_play = series.iloc[next_index]
        return next_play['down'], next_play['ydstogo']

    @staticmethod
    def save_named_table(table, filename, env):
        df = pd.DataFrame(data=table,
                          index=env.space.STATES,
                          columns=[action['title'] for action in env.space.ACTIONS])
        df = df.reset_index()

        # Remove states success and fail
        df = df[~df['index'].isin(['success', 'fail'])]

        # Split the state into down and distance columns
        df['down'] = df['index'].str.split('|', n=1, expand=True)[0]
        df['distance'] = df['index'].str.split('|', n=1, expand=True)[1]
        df = df.drop(columns=['index'])

        # Move down and distance to front of dataframe
        columns = df.columns.tolist()
        columns.remove('down')
        columns.remove('distance')
        columns.insert(0, 'down')
        columns.insert(1, 'distance')
        df = df.loc[:, columns]

        df.to_csv(filename, index=False)

    def learn(self, lr, y, e):
        space_index = 2
        folder = 'results/space' + str(space_index) + '/'
        gym.envs.register(id='FootballSpace-v1',
                          entry_point='dashboard_env:DashboardEnv',
                          kwargs={'space': space_index})

        env = gym.make('FootballSpace-v1')

        # Initialize table with all zeros
        Q = np.zeros([env.observation_space.n, env.action_space.n])
        Q[:, :] = 0
        Q_counts = np.zeros([env.observation_space.n, env.action_space.n])

        # create lists to contain total rewards and steps per episode
        jList = []
        rList = []
        rTotalList = []
        rTotal = 0
        num_series = self.df['series_num'].nunique()
        max_plays = self.df.groupby('series_num').size().max()
        print('Num Series', num_series)
        for i, series in self.df.groupby('series_num'):
            # Reset environment and get first new observation
            s = env.reset()
            rAll = 0
            # The Q-Table learning algorithm
            for p, (_, play) in enumerate(series.iterrows()):
                # Find action by play
                a = env.find_action(play)

                # Get new state and reward from environment
                s1, r, d, _ = env.step((a, play, *(self.get_next_down_distance(series, p))))

                # Update Q-Table with new knowledge
                Q[s, a] += lr * (r + y * np.max(Q[s1, :]) - Q[s, a])
                Q_counts[s, a] += 1

                rAll += r
                rTotal += r
                s = s1

            jList.append(len(series))
            rList.append(rAll)
            rTotalList.append(rTotal)

            if self.verbose:
                if i % 500 == 0:
                    print('episode (series)', i)

        self.save_named_table(Q, folder + 'table_names.csv', env)
        Q_counts = np.sum(Q_counts, axis=1)
        Q_counts = Q_counts.reshape((Q_counts.shape[0], 1))
        Q_counts = np.repeat(Q_counts, Q.shape[1], axis=1)
        self.save_named_table(Q / Q_counts, folder + 'table_names_normalized.csv', env)

        # np.savetxt(folder + 'table.csv', Q, delimiter=',', fmt='%.5f')

        print('Creating Ranked plays')
        ranked_plays = []
        for i, series in self.df.groupby('series_num'):
            s = env.reset()
            current_rewards = []
            for p, (_, play) in enumerate(series.iterrows()):
                # Find action by play
                a = env.find_action(play)

                current_rewards.append(Q[s, a])

                # Get new state and reward from environment
                s1, r, d, _ = env.step((a, play, *(self.get_next_down_distance(series, p))))

                s = s1

            # current_rewards.append(Q[s, a])
            ranked_plays.append(current_rewards)

            if self.verbose:
                if i % 500 == 0:
                    print('episode (series)', i)

        df_ranked_plays = pd.DataFrame(data=ranked_plays,
                                       index=['series' + str(i + 1) for i in range(num_series)],
                                       columns=['play' + str(i + 1) for i in range(max_plays)])
        df_ranked_plays.to_csv(folder + 'ranked_plays.csv')

        if self.verbose:
            print("Score over time: " + str(sum(rList) / num_series))
            print("Average episode length: " + str(np.mean(jList)))
            print("Average last 50 episode length: " + str(np.mean(jList[-50:])))
            print("Final Q-Table Values")
            print(Q)

        avg_r = np.mean(rList[-50:])
        avg_j = np.mean(jList[-50:])

        def movingaverage(interval, window_size):
            window = np.ones(int(window_size)) / float(window_size)
            return np.convolve(interval, window, 'same')

        w_size = 50

        rList = movingaverage(rList, w_size)
        plt.plot(rList)
        r_min = min(rList)
        if r_min < 0:
            r_min *= 1.2
        else:
            r_min *= 0.8
        plt.ylim(r_min, 1.50 * max(rList))
        if self.show_graphs:
            plt.show()

        if self.save_files:
            plt.savefig(folder + 'rSmooth.png')
            plt.close()

        jList = movingaverage(jList, w_size)
        plt.plot(jList)
        j_min = min(jList)
        if j_min < 0:
            j_min *= 1.2
        else:
            j_min *= 0.8
        plt.ylim(j_min, 1.50 * max(jList))
        if self.show_graphs:
            plt.show()

        if self.save_files:
            plt.savefig(folder + 'jSmooth.png')

        return avg_j, avg_r


def main():
    # Regular
    learner = Learner(show_graphs=False, save_files=True, verbose=True)
    learner.learn(lr=0.85, y=0.99, e=0.05)
    exit()

    # Log all possible parameter values
    scatter = {}
    learner = Learner(show_graphs=False, verbose=False)
    for question in range(1, 2):
        if question not in scatter:
            scatter[question] = {'lr': [], 'y': [], 'r': [], 'j': []}

        for lr in [x / 10.0 for x in range(0, 100, 5)]:
            for y in [x / 10.0 for x in range(0, 100, 1)]:
                print(lr, y)
                avg_j, avg_r = learner.learn(lr=lr, y=y, e=0.05)

                scatter[question]['lr'].append(lr)
                scatter[question]['y'].append(y)
                scatter[question]['r'].append(avg_r)
                scatter[question]['j'].append(avg_j)

    with open('scatter.pickle', 'wb') as w:
        json.dump(scatter, w)


if __name__ == '__main__':
    main()
