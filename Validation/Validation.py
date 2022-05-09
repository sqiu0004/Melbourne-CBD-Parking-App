import csv
import math
from collections import defaultdict
import random
from datetime import datetime
import sqlite3
import statistics as stat

N = 20000
con = sqlite3.connect("Data1.db")
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='t'")
if cur.fetchone() is None:
    # Create Buoy ID table
    cur.execute("CREATE TABLE t (BayId, ArrivalTime, DepartureTime, DurationMinutes);")
    with open('data2019_filtered.csv', 'r') as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [(i['BayId'], datetime.strptime(i['ArrivalTime'], '%m/%d/%Y %I:%M:%S %p').timestamp(), datetime.strptime(i['DepartureTime'], '%m/%d/%Y %I:%M:%S %p').timestamp(), i['DurationMinutes']) for i in dr]
    cur.executemany("INSERT INTO t (BayId, ArrivalTime, DepartureTime, DurationMinutes) VALUES (?, ?,?,?);", to_db)
    con.commit()
else:
    print("Table table already exists!")

with open('monthly_table_combined_1.0.csv', newline="") as csvfile:
    columns = defaultdict(list)
    reader = csv.DictReader(csvfile)
    usedBayIds = []
    score = 0
    sample = [[], [], [], [], [], [], [], [], [], [], [], []]

    for row in reader:
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)
with open('monthly_table_combined_1.0.csv', newline="") as csvfile:
    csv_reader = csv.reader(csvfile)
    rows = list(csv_reader)
    headers = []
    for x in range(0, len(rows[0])):
        if x > 2:
            if rows[0][x] != '0':
                headers.append([rows[0][x], x - 3])
    """
    for x in range(2, len(columns)): # making sure that we only test bayId's in which we have data for
        Sum = 0
        for y in columns[str(x)]:
            Sum += float(y)
        if Sum != 0:
            usedBayIds.append(x)
    """
    for n in range(1, N+1):
        index = random.randrange(0, len(headers))
        markerID=headers[index][0]
        bayId = headers[index][1]
        unixTime = random.randrange(1546261200, 1577797199) # random unix time for 2019
        Date = datetime.fromtimestamp(unixTime)
        dayNum = Date.weekday()
        hour = Date.hour#
        month = Date.month -1
        minute = Date.minute
        seconds = Date.second
        timeOccupied = 0
        print("markerID", markerID," bayid ", bayId, " month ",month, " day ", dayNum, " hour ", hour)
        cur.execute("SELECT * FROM t WHERE BayId = ? AND ArrivalTime <? AND DepartureTime> ?", (str(bayId), unixTime, unixTime))
        #df= pd.read_sql_query("SELECT DurationMinutes from t where BayId = 5311 and ArrivalTime <= 1565043480 and DepartureTime>=1565043480" , con)
        if cur.fetchone() is None:
            carParked = 0
        else:
            carParked = 1
        score += (float(columns[str(markerID)][24 * dayNum + month*168 + hour]) / 100 - carParked) ** 2
        core=score/n
        print('n:', n, 'bayId:', bayId, "predicted:", float(columns[str(markerID)][24*dayNum+hour+ month*168])/100, "actual:", carParked, 'currentScore:',core)

        startHour = unixTime - 60*minute - seconds
        endHour = startHour + 3600
        cur.execute("SELECT * FROM t WHERE BayId = ? AND ((ArrivalTime <? AND DepartureTime>?) OR (ArrivalTime >? AND ArrivalTime<?) OR (DepartureTime >? AND DepartureTime<?))", (str(bayId), startHour, endHour, startHour, endHour, startHour, endHour))
        for c in cur.fetchall():
            if c[1] < startHour:
                startTime = startHour
            else:
                startTime = c[1]
            if c[2] > endHour:
                endTime = endHour
            else:
                endTime = c[2]
            timeOccupied += endTime - startTime
        difference = float(columns[str(markerID)][24*dayNum+168*month+hour])/100 - timeOccupied/3600
        #sample.append(difference)
        sample[month].append(difference)
        print("n:", n)
        """
        if n>2:
            sampleMean = stat.mean(sample)
            sampleStd = stat.stdev(sample)
            print("mean", sampleMean, " sd", sampleStd)
        """
    score = score / N
    print('Score', score)
with open("Monthly-1.0.txt", "w") as f:
    for x in sample:
        for item in x:
            f.write("%s#n" % item)
        f.write("\n")
