import pandas as pd


def calculate_conversion_percentages():
    # dataset being used with removed columns
    df = pd.read_csv('../../data/reg_pbp_2018_CarMel_RmvCol_for_firstdown_success.csv')

    df = df[df['play_type'].isin(['no_play', 'pass', 'punt', 'run'])]

    df = df[df['down'].notnull()]

    # Ravens VS Bills to keep it simple
    # df = df[df['game_id'] == 2018090900]

    # df = df[df['qtr'] == 1]

    df = df.reset_index(drop=True)

    df['series_num'] = -1
    df['series_success'] = False

    begin_series_index = 0
    series_num = 1

    # Go through dataframe by rows
    for index, row in df.iterrows():
        if row['game_id'] != df.iloc[index - 1]['game_id'] or (row['qtr'] == 3 and df.iloc[index - 1]['qtr'] == 2):
            if df.iloc[index - 1]['series_num'] == -1:
                df.loc[begin_series_index:index, 'series_num'] = series_num
                df.loc[begin_series_index:index, 'series_success'] = False
                begin_series_index = index
                series_num += 1

        # Success
        if row['first_down_rush'] == 1 or row['first_down_pass'] == 1 or row['first_down_penalty'] == 1 \
                or row['touchdown'] == 1:
            df.loc[begin_series_index:index, 'series_num'] = series_num
            df.loc[begin_series_index:index, 'series_success'] = True
            begin_series_index = index + 1
            series_num += 1

        # Fail
        elif row['fourth_down_failed'] == 1 or row['interception'] == 1 or row['safety'] == 1 or \
                row['fumble_lost'] == 1 or (row['play_type'] == 'punt' and row['penalty'] == 0):
            df.loc[begin_series_index:index, 'series_num'] = series_num
            df.loc[begin_series_index:index, 'series_success'] = False
            begin_series_index = index + 1
            series_num += 1

    # Capture rows at the very end that could have been failures
    df.loc[df['series_num'] == -1, 'series_success'] = False
    df.loc[df['series_num'] == -1, 'series_num'] = series_num

    success_rate = {
    }

    for key in ['all', 'no_goal_line']:
        counts = {
            'Down': [],
            'Distance': [],
            'Success': [],
            'Fail': [],
        }

        for down in range(1, 5):
            for distance in range(1, 47):
                print(down, distance)
                df_sub = df[(df['down'] == down) & (df['ydstogo'] == distance)]
                if key == 'no_goal_line':
                    df_sub = df_sub[df_sub['goal_to_go'] == 0]

                df_sub = df_sub.drop_duplicates('series_num')

                num_success = df_sub[df_sub['series_success']].shape[0]
                num_fail = df_sub[~df_sub['series_success']].shape[0]

                counts['Down'].append(down)
                counts['Distance'].append(distance)
                counts['Success'].append(num_success)
                counts['Fail'].append(num_fail)

        success_rate[key] = pd.DataFrame(counts)
    return success_rate


def __get_raw_percentage(row):
    if row['Success'] + row['Fail'] <= 100:
        return -1

    return row['Success'] / (row['Success'] + row['Fail'])


def __nn_percentage(index, df):
    """
    Compute the nearest neighbor conversion percentage for the row
    :param index: The index of the row to find nearest neighbor for
    :param df: The dataframe to search
    :return: The percentage to set the row to
    """

    neighbor_up = None
    neighbor_down = None
    for i in range(index - 1, -1, -1):
        if df.iloc[i]['Percentage'] != -1:
            neighbor_up = df.iloc[i]['Percentage']
            break

    for i in range(index + 1, df.shape[0]):
        if df.iloc[i]['Percentage'] != -1:
            neighbor_down = df.iloc[i]['Percentage']
            break

    if neighbor_up is None and neighbor_down is None:
        print('Error: Unable to find a nearest neighbor!')
        exit()

    if neighbor_up is None:
        return neighbor_down

    if neighbor_down is None:
        return neighbor_up

    return (neighbor_up + neighbor_down) / 2


def get_clean_percentages():
    import os
    if os.path.exists('temp.csv'):
        df = pd.read_csv('temp.csv')
    else:
        df = calculate_conversion_percentages()['no_goal_line']
        df.to_csv('temp.csv', index=False)

    df['Percentage'] = df.apply(__get_raw_percentage, axis=1)

    # Find rows with -1
    for index, row in df.iterrows():
        if row['Percentage'] == -1:
            df.loc[index, 'Percentage'] = __nn_percentage(index, df)

    return df


def get_clean_percentages_dict():
    df = get_clean_percentages()
    mapping = {}
    for _, row in df.iterrows():
        down = row['Down']
        distance = row['Distance']
        if down not in mapping:
            mapping[down] = {}

        mapping[down][distance] = row['Percentage']

    return mapping


if __name__ == '__main__':
    get_clean_percentages()
