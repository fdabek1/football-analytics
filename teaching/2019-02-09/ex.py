# fruits = ["apple", "banana", "cherry"]
# banana_index = -1
#
# i = 0
# for fruit_name in fruits:
#     print(fruit_name, i)
#     i = i + 1

# if fruit_name == 'apple' or fruit_name == 'banana':
#     print(fruit_name)


# def get_items(fruits_veggies, lowercase=False, uppercase=False):
#     # get all the fruits and return
#     pass

class A:
    def __init__(self):
        self.name = 'something'

    def get_items(self):
        print('in here', self.name)


if __name__ == '__main__':
    a = {
        'all': None,
        1: DATAFRAME HERE,
        2: DATAFRAME HERE,
        3: DATAFRAME HERE,
        4: DATAFRAME HERE,
    }

    df = None

    df = df.sort_values(['GameDate', 'GameId', 'Quarter', 'Minute', 'Second'])

    last_series_index = 0
    for r, row in enumerate(df.iterrows()):
        if row['SeriesFirstDown'] == 1:
            current_series = df.iloc[last_series_index:r+1]
            current_series[current_series['Flag'] != 1].shape
            last_series_index = r + 1


    for series_type, df in a.items():
        pass

    columns = ['a', 'a', 'c']
    data = [1, 2, 3]

    columns = list(set(columns))
    columns = set()
    columns.add('a')
    columns = list() # []
    columns.append('a')
    del df
    blah = A()
    blah.get_items()

# get_items([], uppercase=True)
