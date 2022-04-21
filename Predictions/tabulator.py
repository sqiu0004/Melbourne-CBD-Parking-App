import csv
import time
import datetime
import numpy as np
import pandas as pd


# Initialise table
n_hours = 168
n_bays = 25000
weekly_table = np.zeros((n_hours,n_bays + 2))
weekly_table[:,0] = np.repeat(np.arange(1,8),24)
weekly_table[:,1] = np.tile(np.arange(0,24),7)

# Outputs dates between two dates
def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + datetime.timedelta(n)


def Main():
    data = input("Data file: ")
    # data = "data2018_filtered"

    with open(data + '.csv', 'r') as in_file, open("weekly_table.csv", "w", newline='') as out_file:
        # Writer header
        header = [None]*2500
        header[:2] = ['Day', 'Hour']
        header[2:] = range(2500)
        writer = csv.writer(out_file)
        writer.writerow(header)

        # Read from filtered list
        next(in_file)
        reader = csv.reader(in_file)
        format = "%m/%d/%Y %I:%M:%S %p"
        j = 0

        # reader = [['1', '04/17/2022 11:39:31 PM', '04/19/2022 11:41:49 AM', '2'],
        #           ['1', '04/17/2022 11:39:31 PM', '04/19/2022 11:41:49 AM', '2'],
        #           ['3', '04/18/2022 08:29:31 PM', '04/18/2022 08:39:31 PM', '2']]
        for row in reader:
            j += 1
            if len(row[0]) <= 5:
                print(j)
                # reformat the arrival and departure times in unix
                unix_a = datetime.datetime.strptime(row[1], format)
                unix_d = datetime.datetime.strptime(row[2], format)
                # find the number of hours between the departure and arrival times
                t_span = unix_d - unix_a
                t_span_h = int(divmod(t_span.total_seconds(), 3600)[0]) + 1
                # convert the arrival time to table index (hours in a week)
                DoW_a = pd.Timestamp(unix_a).dayofweek
                hour_a = DoW_a*24 + unix_a.hour
                # increment times of occupancy
                for hour in range(t_span_h):
                    if t_span_h == 1:
                        weekly_table[(hour_a + hour) % n_hours, (int(row[0]) + 2)] += round(unix_d.minute / 10) - round(unix_a.minute / 10)
                    elif hour == 0:
                        weekly_table[(hour_a + hour) % n_hours, (int(row[0]) + 2)] += 6 - round(unix_a.minute / 10)
                    elif hour == t_span_h - 1:
                        weekly_table[(hour_a + hour) % n_hours, (int(row[0]) + 2)] += round(unix_d.minute / 10)
                    else:
                        weekly_table[(hour_a + hour) % n_hours, (int(row[0]) + 2)] += 6

        weekly_table[:,2:] = np.clip(weekly_table[:,2:]*100.0/(52*6.0), 0.0, 100.0)
        writer.writerows(weekly_table)

if __name__ == '__main__':
    Main()