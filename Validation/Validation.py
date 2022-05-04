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

with open('weekly_table_2018-20.csv', newline="") as csvfile:
    columns = defaultdict(list)
    reader = csv.DictReader(csvfile)
    usedBayIds = []
    score = 0
    sample = []
    for row in reader:
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)
    for x in range(2, len(columns)-2): # making sure that we only test bayId's in which we have data for
        Sum = 0
        for y in columns[str(x)]:
            Sum += float(y)
        if Sum != 0:
            usedBayIds.append(x)
    for n in range(1, N):
        index = random.randrange(0, len(usedBayIds))
        bayId = usedBayIds[index]
        unixTime = random.randrange(1546261200, 1577797199) # random unix time for 2019
        Date = datetime.fromtimestamp(unixTime)
        dayNum = Date.weekday()
        hour = Date.hour
        minute = Date.minute
        seconds = Date.second
        timeOccupied = 0
        cur.execute("SELECT * FROM t WHERE BayId = ? AND ArrivalTime <? AND DepartureTime> ?", (str(bayId), unixTime, unixTime))
        #df= pd.read_sql_query("SELECT DurationMinutes from t where BayId = 5311 and ArrivalTime <= 1565043480 and DepartureTime>=1565043480" , con)
        if cur.fetchone() is None:
            carParked = 0
        else:
            carParked = 1
        score += (float(columns[str(bayId)][24 * dayNum + hour]) / 100 - carParked) ** 2
        core=score/n
        print('n:', n, 'bayId:', bayId, "predicted:", float(columns[str(bayId)][24*dayNum+hour])/100, "actual:", carParked, 'currentScore:',core)
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
        difference = float(columns[str(bayId)][24*dayNum+hour])/100 - timeOccupied/3600
        sample.append(difference)
        if n>2:
            sampleMean = stat.mean(sample)
            sampleStd = stat.stdev(sample)
            print("mean", sampleMean, " sd", sampleStd)
    score = score / N
    print('Score', score)
with open("sampledata.txt", "w") as f:
    for item in sample: 
        f.write("%s#n" % item)
