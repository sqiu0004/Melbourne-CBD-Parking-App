import csv
import datetime
import numpy as np


params = ['Month', 'Day', 'Hour']  # parameters
DiW = 7  # Days in week
HiD = 24  # Hours in day
MiY = 12  # Months in the year
n_hours = DiW * HiD * MiY


def daterange(date1, date2):
    """Outputs dates between two dates"""
    for n in range(int((date2 - date1).days)+1):
        yield date1 + datetime.timedelta(n)


def id_list_init(path = "D:/Desktop/Academia/TRC4200/results/id_table.csv"):
    """Converts list of marker ids to list"""
    with open(path, 'r') as id_file:
        next(id_file)
        id_reader = csv.reader(id_file, delimiter=',', quotechar="'")
        markerId_list = [row[1:] for row in id_reader]
        markerId_list = markerId_list[0]

    return markerId_list


def table_init(markerId_list):
    """Instantiates probability table"""
    n_ids = len(markerId_list)
    weekly_table = np.zeros((n_hours, n_ids + len(params)))  # monthly column
    weekly_table[:, 0] = np.repeat(np.arange(0, MiY) + 1, DiW * HiD)  # monthly column
    weekly_table[:, 1] = np.tile(np.repeat(np.arange(0, DiW) + 1, HiD), MiY)  # weekly column
    weekly_table[:, 2] = np.tile(np.arange(0, HiD), DiW * MiY)  # hourly coloumn

    return weekly_table


def header_init(markerId_list):
    """Instantiates header of .csv file"""
    header = [None for i in range(n_hours+len(params))]
    header[:len(params)] = params
    header[len(params):] = markerId_list

    return header


def merge_tables(header, weekly_table):
    """Merges two tables together"""
    table1 = input("table 1: ")  # D:\Desktop\Academia\TRC4200\results\baseline_table.csv
    table2 = input("Table 2: ")  # D:\Desktop\Academia\TRC4200\results\monthly_table_2018-20_MarkerId.csv
    ratio = input("Ratio (0.0-1.0): ")

    with open(table1, 'r') as in_file1, open(table2, 'r') as in_file2, open("monthly_table_combined_" + ratio + ".csv", "w", newline='') as out_file:
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

        for i in range(weekly_table.shape[0]):
            for counter in range(len(params), weekly_table.shape[1]):
                if (data1[i, counter] < 1.0) or (data2[i, counter] < 1.0):
                    weekly_table[i, counter] = data1[i, counter] + data2[i, counter]
                else:
                    weekly_table[i, counter] = data1[i, counter]*(1.0 - float(ratio)) + data2[i, counter]*float(ratio)

        writer.writerows(weekly_table)


def tabulate_probabilities(header, weekly_table):
        data = input("Data file: ")
        # e.g. D:\Desktop\Academia\TRC4200\data_2016-20_filtered\data2017_filtered.csv
        monthly = False
        month = False

        while True:
            monthly = input("Choose specific month? (y/n):")
            if monthly == "y":
                monthly = True
                month = input("Enter month (1-12): ")
                break
            elif monthly == "n":
                monthly = False
                break
            else:
                print("Answer must be (y/n)!")

        with open(data, 'r') as in_file, open("monthly_table.csv", "w", newline='') as out_file:
            # Writer header
            writer = csv.writer(out_file)
            writer.writerow(header)

            # Read from filtered list
            next(in_file)
            reader = csv.reader(in_file)
            format = "%m/%d/%Y %I:%M:%S %p"
            earliest_date = None
            latest_date = None
            counter = 0
            discarded = 0

            for row in reader:
                # Row elements
                id = row[0]
                time_a = row[1]  # arrival time
                time_d = row[2]  # departure time
                m_span = row[len(params)]  # time difference in minutes

                # Reformat the arrival and departure times in unix
                unix_a = datetime.datetime.strptime(time_a, format)
                unix_d = datetime.datetime.strptime(time_d, format)

                if unix_a.month != unix_d.month:
                    discarded += 1
                    continue
                if monthly:
                    if (int(unix_a.month) != int(month)) or (int(unix_d.month) != int(month)):
                        continue

                # find earliest and latest dates
                # arrival time is used to compare b/c some departure dates are outliers
                counter += 1
                if counter == 1:
                    earliest_date = unix_a
                    latest_date = unix_a
                else:
                    earliest_date = earliest_date if (earliest_date - unix_a).days < 0 else unix_a
                    latest_date   = latest_date   if (latest_date   - unix_a).days > 0 else unix_a

                # find the number of hours between the departure and arrival times
                h_span = (datetime.datetime.combine(unix_d.date(), datetime.time(unix_d.hour)) -
                          datetime.datetime.combine(unix_a.date(), datetime.time(unix_a.hour)))
                h_span = int(1 + h_span.total_seconds()/3600)

                # convert the arrival time to table index (hours in a week)
                DoW_a = unix_a.weekday()
                MoY_a = unix_a.month - 1
                HiW = HiD*DiW
                print(counter, ":   bay(", id, ")   arr(", unix_a, ")   dep(", unix_d, ")   h_span(", h_span, ")    discarded(", discarded, ")")

                # increment times of occupancy
                if h_span == 1:  # if event *only occupies one hour* take the difference between departure and arrival minutes
                    hour_a = MoY_a * HiD * DiW + ((DoW_a * HiD + unix_a.hour) % HiW)
                    weekly_table[hour_a, (int(id) + len(params))] += round(unix_d.minute / 10) - round(unix_a.minute / 10)
                else:
                    for hour in range(h_span):
                        hour_a = MoY_a*HiD*DiW + ((DoW_a*HiD + unix_a.hour + hour) % HiW)
                        if hour == 0:  # if event is over one hour, take the time occupied in the first hour using the arrival time
                            weekly_table[hour_a, (int(id) + len(params))] += 6 - round(unix_a.minute / 10)
                        elif hour == h_span - 1:  # if event is over one hour, take the time occupied in the last hour using the departure time
                            weekly_table[hour_a, (int(id) + len(params))] += round(unix_d.minute / 10)
                        else:  # if event is over one hour, assume all hours in between arrival and departure are occupied completely
                            weekly_table[hour_a, (int(id) + len(params))] += 6

            weekly_table[:,len(params):] = np.clip(weekly_table[:,len(params):]*100.0/(((365.25/12.0)/7.0)*6.0), 0.0, 100.0)  # calculate the percentage
            writer.writerows(weekly_table)


def Main():
    # Initialise marker id list
    markerId_list = id_list_init("D:/Desktop/Academia/TRC4200/results/id_table.csv")
    # Initialise probability table
    weekly_table = table_init(markerId_list)
    # Create header
    header = header_init(markerId_list)

    option = input("1. Tabulate probability \n2. Merge probability tables\n Choose option: ")
    if option == "2":
        merge_tables(header, weekly_table)

    elif option == "1":
        tabulate_probabilities(header, weekly_table)

if __name__ == '__main__':
    Main()