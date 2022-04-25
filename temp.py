import csv
import pandas as pd
import datetime
import time
import numpy as np


def Main():
    t1 = datetime.datetime(2022, 4, 25, 22, 35, 0)
    t1_date = t1.date()
    t1_hour = datetime.time(t1.hour)
    t1_combine = datetime.datetime.combine(t1_date, t1_hour)

    t2 = datetime.datetime(2022, 4, 25, 23, 50, 0)
    t2_date = t2.date()
    t2_hour = datetime.time(t2.hour)
    t2_combine = datetime.datetime.combine(t2_date, t2_hour)

    print((t1_combine - t2_combine).total_seconds()/3600)
    for i in range(1):
        print(i)

if __name__ == '__main__':
    Main()
