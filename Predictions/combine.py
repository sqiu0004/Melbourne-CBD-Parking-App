import numpy as np
import plotly.express as px
import pandas as pd
from datetime import datetime


def modify_df(csv_filename):
    #time arrive, time depart, duration, bayid, VehiclePresent
    df = pd.read_csv(csv_filename,usecols=[1,2,3,16,18]) 
    df_mod = df[df.DurationMinutes != 0]
    
    df_mod['Dates'] = pd.to_datetime(df['ArrivalTime']).dt.date
    df_mod['Time arrive'] = pd.to_datetime(df['ArrivalTime']).dt.time
    df_mod['Time depart'] = pd.to_datetime(df['DepartureTime']).dt.time
    df_mod['month']= pd.to_datetime(df['ArrivalTime']).dt.month
    df_mod['day of week'] = pd.to_datetime(df['DepartureTime']).dt.dayofweek
    
    df_mod.to_csv('modified.csv', index=False, mode='w+')
    return df_mod

def extract_and_predict(df, time_now, dayofweek, month): #can also put bay_id for parameter
    #convert string to date.datetime
    time_now = datetime.strptime(time_now, '%H:%M:%S').time()
    #get time from df
    df = df.loc[(df['Time arrive'] < time_now) & 
    (df['Time depart'] > time_now) & 
    (df['day of week'] == dayofweek) & 
    (df['month'] == month)]

    print(df)
    total_occupied = df['VehiclePresent'].sum()
    length = df.shape[0]
    prediction = round(100 - (total_occupied / length * 100), 1)
    # prediction = round(prediction, 1)
    print('total spot: %d' % length)
    print('num of occupied spot: %d' % total_occupied)
    print('unoccupied: %0.1f%%' % prediction)
    # df.to_csv('combine.csv', index=False, mode='w+')
    # print(prediction)
    return prediction

# def predict_whole_year():
#     store = []
#     for month in range(1): 
#         for date in range(31):
#             for time in range(8,20):#8am to 7pm
#                 hour = str(time)+":00:00"
#                 predic = extract_and_predict(df,hour,date+1,month+3)
#                 store.append(np.array([time, date+1, month+3, predic]))
#     np.savetxt('wholeyear.csv', store, fmt='%.1f', delimiter=',')
#     return store


filename = 'march_bay1200.csv'
df = modify_df(filename)
pred = extract_and_predict(df,"9:00:00",2,3) #time, date, month, bayid, other

store = []
for month in range(1): 
    for date in range(31):
        for time in range(8,20):#8am to 7pm
            hour = str(time)+":00:00"
            predic = extract_and_predict(df,hour,date+1,month+3)
            store.append(np.array([time, date+1, month+3, predic]))
np.savetxt('wholeyear.csv', store, fmt='%.1f', delimiter=',')


# timeNow = '9:11:00'
# timeNow = datetime.strptime(timeNow, '%H:%M:%S').time()

# df1 = df.loc[(df['Time arrive'] < timeNow) & (df['Time depart'] > timeNow)]
# print(df1['Time arrive','Time depart','VehiclePresent', 'Dates'])
# # df2 = df.loc[df['VehiclePresent'] == 1]
# total_occupied = df1['VehiclePresent'].sum()
# length = df1.shape[0]
# prediction = 100 - (total_occupied / length * 100)
# prediction = round(prediction, 1)
# print(length)
# print(total_occupied)
# print(prediction)

# a = 11
# c = str(a)+":00:00"