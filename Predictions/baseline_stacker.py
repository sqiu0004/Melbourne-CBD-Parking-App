import csv
import datetime
import numpy as np


# Initialise table
id_list = range(0,10000)
params = ['Month', 'Day', 'Hour']  # parameters
DiW = 7  # Days in week
HiD = 24  # Hours in day
MiY = 12  # Months in the year
n_hours = DiW*HiD*MiY
n_ids = len(id_list)
weekly_table = np.zeros((n_hours,n_ids + len(params)))  # monthly column
weekly_table[:, 0] = np.repeat(np.arange(0,MiY)+1,DiW*HiD)  # monthly column
weekly_table[:, 1] = np.tile(np.repeat(np.arange(0,DiW)+1,HiD),MiY)  # weekly column
weekly_table[:, 2] = np.tile(np.arange(0,HiD),DiW*MiY) # hourly coloumn


# Outputs dates between two dates
def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + datetime.timedelta(n)


def Main():
    header = [None for i in range(n_hours+len(params))]
    header[:len(params)] = params
    header[len(params):] = id_list

    data = input("Data file: ")
    # e.g. "D:\Desktop\TRC4200\data2018-20_filtered\data2020_filtered"
    monthly = False
    month = False

    with open("baseline_table.csv", "w", newline='') as out_file:
        # Writer header
        writer = csv.writer(out_file)
        writer.writerow(header)

        j = 0
        for month in range(MiY):

            with open(data + '.csv', 'r') as in_file:
                # Read from filtered list
                next(in_file)
                reader = csv.reader(in_file)

                for row in reader:
                    weekly_table[j,len(params):] = [ float(i) for i in row[2:10002] ]
                    j += 1

        writer.writerows(weekly_table)

if __name__ == '__main__':
    Main()