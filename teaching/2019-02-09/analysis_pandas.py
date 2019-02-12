import pandas as pd

df = pd.read_csv('../../data/pbp-2018.csv')

# df = df[df['GameId'] == 2018090900]
# df = df[df['OffenseTeam'] == 'BAL']

# print(df.shape)
# print(df['OffenseTeam'].value_counts())
print(df['OffenseTeam'])
print(df['OffenseTeam'].isna())

print(df[df['OffenseTeam'].isna()])
print(df[df['OffenseTeam'].isna()].shape)


# print(df[(df['Quarter'] == 1) & (df['Minute'] == 2)])


print(df)


# print(df[df['Quarter'].isin([1, 2])])

