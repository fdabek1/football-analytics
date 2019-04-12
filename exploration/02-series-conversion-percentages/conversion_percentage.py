import pandas as pd


# TODO - Check for field goals (they should be failures) (Qtr 2 at 6:04)  (Qtr 4 at 2:13)
# TODO - Remove series at end of game and end of half

def calculate_conversion_percentages():
    # dataset being used with removed columns
    df = pd.read_csv('../../data/reg_pbp_2018_CarMel_RmvCol_for_firstdown_success.csv')
    max_yds_to_go = df['ydstogo'].max()

    df = df[df['play_type'].isin(['no_play', 'pass', 'punt', 'run', 'field_goal', 'qb_kneel', 'qb_spike'])]

    df = df[df['down'].notnull()]

    # Ravens VS Bills to keep it simple
    # df = df[df['game_id'] == 2018090900]

    # df = df[df['qtr'] == 1]

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
                print('delete', df.loc[begin_series_index:index - 1][['qtr', 'time']])
                begin_series_index = index
                # series_num += 1

        # Success
        if row['first_down_rush'] == 1 or row['first_down_pass'] == 1 or row['first_down_penalty'] == 1 \
                or row['touchdown'] == 1:
            df.loc[begin_series_index:index, 'series_num'] = series_num
            df.loc[begin_series_index:index, 'series_success'] = True
            print('success', df.loc[begin_series_index:index][['qtr', 'time']])
            begin_series_index = index + 1
            series_num += 1

        # Fail
        elif row['fourth_down_failed'] == 1 or row['interception'] == 1 or row['safety'] == 1 or \
                row['fumble_lost'] == 1 or (row['play_type'] == 'punt' and row['penalty'] == 0) or \
                row['play_type'] == 'field_goal':
            df.loc[begin_series_index:index, 'series_num'] = series_num
            df.loc[begin_series_index:index, 'series_success'] = False
            print('fail', df.loc[begin_series_index:index][['qtr', 'time']])
            begin_series_index = index + 1
            series_num += 1

    # Delete end of half and end of game series
    df = df[~df['series_delete']]

    # Capture rows at the very end that could have been failures
    # print('after', df.loc[df['series_num'] == -1][['qtr', 'time']])
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
            for distance in range(1, max_yds_to_go + 1):
                print(down, distance)
                df_sub = df[(df['down'] == down) & (df['ydstogo'] == distance)]
                df_sub = df_sub[df_sub['play_type'] != 'punt']
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
    with pd.ExcelWriter('conversion_percentages_ravens_saints_2018102101.xlsx') as writer:
        for key, value in success_rate.items():
            value.to_excel(writer, sheet_name=key, index=False)


if __name__ == '__main__':
    results = calculate_conversion_percentages()
    # write_file(results)
