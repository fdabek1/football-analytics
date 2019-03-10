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
                row['fumble_lost'] == 1 or (row['play_type'] == 'punt' and row['penalty'] == 0) or ():
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
            for distance in range(1, 30):
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


def write_file(success_rate):
    with pd.ExcelWriter('conversion_percentages.xlsx') as writer:
        for key, value in success_rate.items():
            value.to_excel(writer, sheet_name=key, index=False)


if __name__ == '__main__':
    results = calculate_conversion_percentages()
    # write_file(results)
