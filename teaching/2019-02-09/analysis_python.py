import csv

with open('../../data/pbp-2018.csv') as f:
    reader = csv.reader(f)
    columns = next(reader)
    print(columns)
    game_id_index = -1
    for x in columns:
        if x == 'Quarter':
            print(x)
    print(game_id_index)
    exit()

    print('BELOW IS THE DATA')
    for line in reader:

        # print(line[3])
        if line[0] == '2018090900':
            print(line)

        # exit()


