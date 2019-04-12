import pandas as pd

from exploration.e02_series_conversion_percentages.conversion_percentage import calculate_conversion_percentages


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
