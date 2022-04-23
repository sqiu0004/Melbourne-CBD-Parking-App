import csv
import datetime
import numpy as np
import pandas as pd


# Initialise table
id_list = range(0,25000)
DiW = 7  # Days in week
HiD = 24  # Hours in day
n_hours = DiW*HiD
n_ids = len(id_list)
weekly_table = np.zeros((n_hours,n_ids + 2))
weekly_table[:,0] = np.repeat(np.arange(0,DiW)+1,HiD)
weekly_table[:,1] = np.tile(np.arange(0,HiD),DiW)


# Outputs dates between two dates
def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + datetime.timedelta(n)


def Main():
    header = [None]*(n_ids+2)
    header[:2] = ['Day', 'Hour']
    header[2:] = id_list

    option = input("1. Tabulate probability \n2. Merge probability tables\n Choose option: ")
    if option == "2":
        table1 = input("table 1: ")
        table2 = input("Table 2: ")

        with open(table1 + '.csv', 'r') as in_file1, open(table2 + '.csv', 'r') as in_file2, open("weekly_table_combined.csv", "w", newline='') as out_file:
            # Writer header
            writer = csv.writer(out_file)
            writer.writerow(header)

            next(in_file1)
            next(in_file2)
            reader1 = csv.reader(in_file1)
            reader2 = csv.reader(in_file2)

            in_file1 = list(reader1)
            in_file2 = list(reader2)
            data1 = np.array(in_file1).astype(float)
            data2 = np.array(in_file2).astype(float)
            data_avg = np.zeros(data1.shape)

            for i in range(data_avg.shape[0]):
                for j in range(data_avg.shape[1]):
                    if (data1[i,j] < 1.0) or (data2[i,j] < 1.0):
                        data_avg[i,j] = data1[i,j]+data2[i,j]
                    else:
                        data_avg[i,j] = (data1[i,j]+data2[i,j])/2

            writer.writerows(data_avg)

    elif option == "1":
        data = input("Data file: ")
        # e.g. "data2018_filtered"

        with open(data + '.csv', 'r') as in_file, open("weekly_table.csv", "w", newline='') as out_file:
            # Writer header
            writer = csv.writer(out_file)
            writer.writerow(header)

            # Read from filtered list
            next(in_file)
            reader = csv.reader(in_file)
            format = "%m/%d/%Y %I:%M:%S %p"
            earliest_date = None
            latest_date = None
            j = 0

            for row in reader:
                j += 1
                print(j)

                # Row elements
                id = row[0]
                time_a = row[1]  # arrival time
                time_d = row[2]  # departure time

                # reformat the arrival and departure times in unix
                unix_a = datetime.datetime.strptime(time_a, format)
                unix_d = datetime.datetime.strptime(time_d, format)

                # find earliest and latest dates
                if j == 1:
                    earliest_date = unix_a
                    latest_date = unix_a
                else:
                    earliest_date = earliest_date if (earliest_date - unix_a).days < 0 else unix_a
                    latest_date   = latest_date   if (latest_date   - unix_a).days > 0 else unix_a

                # find the number of hours between the departure and arrival times
                t_span = unix_d - unix_a
                t_span_h = int(divmod(t_span.total_seconds(), 3600)[0]) + 1

                # convert the arrival time to table index (hours in a week)
                DoW_a = pd.Timestamp(unix_a).dayofweek
                hour_a = DoW_a*24 + unix_a.hour

                # increment times of occupancy
                for hour in range(t_span_h):
                    if t_span_h == 1:  # if event *only occupies one hour* take the difference between departure and arrival minutes
                        weekly_table[(hour_a + hour) % n_hours, (int(id) + 2)] += round(unix_d.minute / 10) - round(unix_a.minute / 10)
                    elif hour == 0:  # if event is over one hour, take the time occupied in the first hour using the arrival time
                        weekly_table[(hour_a + hour) % n_hours, (int(id) + 2)] += 6 - round(unix_a.minute / 10)
                    elif hour == t_span_h - 1: # if event is over one hour, take the time occupied in the last hour using the departure time
                        weekly_table[(hour_a + hour) % n_hours, (int(id) + 2)] += round(unix_d.minute / 10)
                    else: # if event is over one hour, assume all hours in between arrival and departure are occupied completely
                        weekly_table[(hour_a + hour) % n_hours, (int(id) + 2)] += 6

            total_weeks = (latest_date - earliest_date).days/7
            print("Total weeks: ", total_weeks)
            weekly_table[:,2:] = np.clip(weekly_table[:,2:]*100.0/(total_weeks*6.0), 0.0, 100.0)  # calculate the percentage by dividing by 52*6 (number of weeks in a year * max number of increments in each element) and clipping the result between 0 and 100%
            writer.writerows(weekly_table)

if __name__ == '__main__':
    Main()