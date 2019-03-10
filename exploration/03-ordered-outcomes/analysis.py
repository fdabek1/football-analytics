from first_down_percentages import get_clean_percentages_dict
import pandas as pd


def rank_plays(df):
    df_original = df
    df_original['RankMethod'] = ''
    new_indices = []

    # Touchdowns Longest to Shortest (Tiebreaker is Conversion Percentage lowest to highest)
    touchdowns = df[(df['touchdown'] == 1) & (df['td_team'] == df['posteam'])]
    touchdowns = touchdowns.sort_values(['yards_gained', 'ConversionPercentage'], ascending=[False, True])
    indices = touchdowns.index.tolist()
    df_original.loc[indices, 'RankMethod'] = 'Touchdown'
    new_indices += indices
    df = df.drop(indices)

    # First Downs Longest to Shortest (Tiebreaker is Conversion Percentage lowest to highest)
    first_downs = df[(df['first_down_rush'] == 1) | (df['first_down_pass'] == 1) | (df['first_down_penalty'] == 1)]
    first_downs = first_downs.sort_values(['yards_gained', 'ConversionPercentage'], ascending=[False, True])
    indices = first_downs.index.tolist()
    df_original.loc[indices, 'RankMethod'] = 'FirstDown'
    new_indices += indices
    df = df.drop(indices)

    turnovers = df[
        (df['fourth_down_failed'] == 1) | (df['interception'] == 1) | (df['safety'] == 1) | (df['fumble_lost'] == 1)]

    # All plays that aren't turnovers - Conversion Percentage lowest to highest
    other_plays = df[~df.index.isin(turnovers.index)]
    other_plays = other_plays.sort_values(['ConversionPercentage', 'yards_gained'], ascending=[True, False])
    indices = other_plays.index.tolist()
    df_original.loc[indices, 'RankMethod'] = 'RegularPlay'
    new_indices += indices
    df = df.drop(indices)

    # Turnovers - Conversion Percentage lowest to highest
    turnovers = turnovers.sort_values('ConversionPercentage', ascending=True)
    indices = turnovers.index.tolist()
    df_original.loc[indices, 'RankMethod'] = 'Turnover'
    new_indices += indices
    df = df.drop(indices)

    print('Should be 0', len(df))

    return df_original.reindex(new_indices)


def main():
    # Sort by:
    # Touchdowns Longest to Shortest
    # First Downs Longest to Shortest
    # Plays by Highest First Down Percentage
    # Turnovers
    df = pd.read_csv('../../data/reg_pbp_2018_CarMel_RmvCol_for_firstdown_success.csv')
    df = df[df['play_type'].isin(['no_play', 'pass', 'punt', 'run'])]
    df = df[df['down'].notnull()]
    df = df.reset_index(drop=True)

    conversion_percentages = get_clean_percentages_dict()

    # Remove punts
    df = df[~((df['play_type'] == 'punt') & (df['penalty'] == 0))]

    df['ConversionPercentage'] = df.apply(lambda row: conversion_percentages[row['down']][row['ydstogo']], axis=1)

    df = rank_plays(df)
    df = df[[
        'RankMethod',
        'down', 'ydstogo', 'yards_gained',
        'first_down_rush', 'first_down_pass', 'first_down_penalty',
        'fourth_down_failed', 'interception', 'safety', 'fumble_lost',
        'play_id',
    ]]
    df.to_csv('plays_ranked_all.csv', index=False)


if __name__ == '__main__':
    main()
