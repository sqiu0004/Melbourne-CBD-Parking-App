import csv
import pandas as pd

# data2019.csv --> 22591813
# data2019_filtered_old.csv --> 22591812
# data2019_filtered.csv -->


def IdTable():
    ids = []
    geom = []

    with open('parking_bay_table.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] != "the_geom":
                ids.append(row[3])
                geom.append(row[0])

        ids_int = [int(id) for id in ids]

    return ids, geom, ids_int


def Main():
    reader = pd.read_csv('data2019_filtered_old.csv')
    print("data2019_filtered_old.csv: ", len(reader))

    # with open('data2019.csv', 'r') as inp:
    #     i = 0
    #     for row in csv.reader(inp):
    #         if row[-1] != "false":
    #             i = i + 1
    #             print(i)


if __name__ == '__main__':
    Main()