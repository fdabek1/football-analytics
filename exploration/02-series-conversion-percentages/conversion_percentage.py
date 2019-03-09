import pandas as pd

# dataset being used with removed columns
df = pd.read_csv('../../data/reg_pbp_2018_CarMel_RmvCol_for_firstdown_success.csv')

df = df[df['play_type'].isin(['no_play', 'pass', 'punt', 'run'])]

df = df[df['down'].notnull()]

# Ravens VS Bills to keep it simple
# df = df[df['game_id'] == 2018090900]

df = df[df['qtr'] == 1]

df = df.reset_index(drop=True)

# stored all series
all_series_success = []
all_series_fail = []

# variable for iloc
index_set = 0

success_rate = {
}

for key in ['all', 'no_goal_line']:
    counts = {
        'Down': [],
        'Distance': [],
        'Success': [],
        'Fail': [],
    }
    if key == 'no_goal_line':
        df = df[df['goal_to_go'] == 0]

    df = df.reset_index(drop=True)

    # Go through dataframe by rows
    for index, row in df.iterrows():
        # Checking if it is the end of a series no matter success or not
        # if successful series
        if row['first_down_rush'] == 1 or row['first_down_pass'] == 1 or row['first_down_penalty'] == 1 \
                or row['touchdown'] == 1:
            # update end of series to index where series stops
            all_series_success.append(df.iloc[index_set:index + 1])
            index_set = index + 1
        else:
            # add failed series here
            if row['fourth_down_failed'] == 1 or row['interception'] == 1 or row['safety'] == 1 or \
                    row['fumble_lost'] == 1 or (row['play_type'] == 'punt' and row['penalty'] == 0):
                all_series_fail.append(df.iloc[index_set:index + 1])
                index_set = index + 1

    for down in range(1, 5):
        for distance in range(1, 30):
            print(down, distance)
            num_success = 0
            num_fail = 0

            # Loop through the all_series_success and count how many success there were
            for series in all_series_success:
                # check for combo of down and distance in series, then add to count
                series_match = series[(series['down'] == down) & (series['ydstogo'] == distance)]
                if len(series_match) > 0:
                    num_success += 1

                # check for all_series fail to count how many fails there were
            for series in all_series_fail:
                series_match = series[(series['down'] == down) & (series['ydstogo'] == distance)]
                if len(series_match) > 0:
                    num_fail += 1

            # print out success rate
            counts['Down'].append(down)
            counts['Distance'].append(distance)
            counts['Success'].append(num_success)
            counts['Fail'].append(num_fail)

    success_rate[key] = pd.DataFrame(counts)

with pd.ExcelWriter('output.xlsx') as writer:
    for key, value in success_rate.items():
        value.to_excel(writer, sheet_name=key, index=False)
