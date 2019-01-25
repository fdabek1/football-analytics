import pandas as pd
import numpy as np
import json

df = pd.read_csv('../../data/drives.csv')


def plays_run(text):
    text = text.split('P ')[1]
    text = text.split(' R')[0]
    return int(text)


def plays_pass(text):
    text = text.split(' P')[0]
    text = text.split('(')[1]
    return int(text)


df['Plays_Run'] = df['Plays'].apply(plays_run)
df['Plays_Pass'] = df['Plays'].apply(plays_pass)
df['Plays_Total'] = df['Plays'].apply(lambda x: int(x.split(' ')[0]))

teams = sorted(df['Tm'].unique().tolist())

print(teams)

bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 14, 22]
bin_text = ['0', '1', '2', '3', '4', '5', '6', '7', '8-10', '10-13', '14+']

data = {'BAL': {'offense': [1, 2, 3, 4], 'defense': [1, 2, 3, 4]}}

max_num = 0
for team in teams:
    offense = df[df['Tm'] == team]
    offense_plays = offense['Plays_Total'].values
    offense_plays = np.histogram(offense_plays, bins=bins)[0]
    offense_plays = offense_plays / sum(offense_plays)
    if max(offense_plays) > max_num:
        max_num = max(offense_plays)

    defense = df[df['Opp'] == team]
    defense_plays = defense['Plays_Total'].values
    defense_plays = np.histogram(defense_plays, bins=bins)[0]
    defense_plays = defense_plays / sum(defense_plays)
    if max(defense_plays) > max_num:
        max_num = max(defense_plays)

    values = []

    for b, num in enumerate(offense_plays):
        values.append({'Bin': bin_text[b], 'Value': num})

    for b, num in enumerate(defense_plays):
        values.append({'Bin': bin_text[b], 'Value': -1 * num})

    data[team] = values

print(max_num)
print(data)

with open('data.json', 'w') as w:
    json.dump(data, w)
