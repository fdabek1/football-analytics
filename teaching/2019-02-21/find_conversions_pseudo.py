import pandas as pd

# Read the dataframe
df = pd.read_csv('')

# Sort it just in case
df = df.sort_values()

# Limit to Ravens-Bills game (just for testing)
df = df[df['game_id'] == 1]

# Store all series
all_series_success = []
all_series_fail = []

# Go through dataframe rows
for index, row in df.iterrows():
    # Check if it is the end of the series
    if True:
        # If it is the end of the series then get the series using df.iloc
        # Determine if the series was a success or not (based on if a first down was achieved or not)
        # Put the series (the set of rows) into the correct all_series list
        # Example: all_series_success.append(df.iloc[])   <--- have to fill in .iloc
        # The .iloc will be just like what was doing before
        pass

# Ok now we have a list of all of the series that were successful and those that were not
# So now need to get all of the combinations and get the success rate
# Like 1st & 1, 1st & 2, 1st & 3, etc.
for down in range(1, 5):  # Looping from 1 to 4
    for distance in range(1, 30):  # Looping from 1 to 30
        num_success = 0
        num_fail = 0

        # Now loop through the all_series_success and count how many success there were
        for series in all_series_success:
            # Check if the down and distance occurs in the series.  If so then add to the count
            if True:
                pass

        # Do the same thing for all_series fail to count how many fails there were
        pass

        # Print out the success rate
        print(str(down) + ' & ' + str(distance) + ': ', num_success, 'out of', num_success + num_fail)
