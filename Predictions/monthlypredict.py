import numpy as np
import calendar
import pandas as pd
from datetime import datetime
import csv
import time

#output all relevant bayid of that specific time, date and month
def extract_and_predict(df, time_now,dayofweek,month): #time, dayofweek, month
    start_time = time.time() #set timer
    #convert string to date.datetime
    time_now = datetime.strptime(time_now, '%H:%M:%S').time()
    #get time from df
    #check if time is in same period
    df_extract = df.loc[
    (pd.to_datetime(df['ArrivalTime']).dt.time < time_now) & 
    (pd.to_datetime(df['DepartureTime']).dt.time > time_now) & 
    (pd.to_datetime(df['DepartureTime']).dt.dayofweek == dayofweek) & 
    (pd.to_datetime(df['ArrivalTime']).dt.month == month)
    ]
    print("---func %s seconds ---" % (time.time() - start_time)) #get time
    print(df_extract)
    return df_extract



filename = 'data2018_filtered.csv'
# filename = 'smaller2018.csv'
num_bayid = 8249
store = np.zeros((2016,num_bayid+3))
# initialize pd (sort data and remove 'durationminute' < 5)
df = pd.read_csv(filename, low_memory=False)
df = df.sort_values(by=['BayId'])
df = df[df.DurationMinutes > 5] 
row = 0
for month in range(1,13): 
    print('month: %d' % month)
        # for date in range(1,32):
    for timeofday in range(24):#0am to 11pm
        for dayofweek in range(7): #0: Mon - 6:Sun
            hour = str(timeofday)+":00:00"
            df_extract = extract_and_predict(df,hour,dayofweek,month)
            store[row,0:3] = [month, timeofday, dayofweek]
            for bayid in range(num_bayid): #extract each bayid one by one from the df_extract
                # in_time = time.time()
                df_temp = df_extract.loc[(df_extract['BayId'] == bayid)] #store relevant bayid in df_temp
                if not df_temp.empty:
                    print(df_temp)
                total_occupied = df_temp.shape[0]
                #check how many Mon/any day in that specific month
                total_date = len([1 for i in calendar.monthcalendar(2018, month) if i[dayofweek] != 0]) 
                if total_occupied>0:
                    print(bayid,total_occupied,total_date)
                #store prediction in monthly table
                store[row,bayid+3] = round(100 - (total_occupied / total_date * 100), 1) #output percentage of unoccupied 
                # print("---done extract bay %d in %s seconds ---" % (bayid, time.time() - in_time))
            row+=1
            print('row: %d' % row)
with open("monthly_table.csv", "w", newline='') as out_file:
    # Writer header
    header = [None]*num_bayid
    header[:3] = ['month', 'time', 'dayofweek']
    header[3:] = range(num_bayid)
    writer = csv.writer(out_file)
    writer.writerow(header)
    for line in range(store.shape[0]):
        writer.writerow(store[line,:])

# print(store)
