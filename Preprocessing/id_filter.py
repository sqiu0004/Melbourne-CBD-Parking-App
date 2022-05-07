import csv
import pandas as pd
import datetime
import time
import numpy as np

IdList = [[0]*(10000+1) for i in range(2)]
for i in range(10000): IdList[0][i+1] = i
BayId = None
MarkerId = None

def Main():
    # data = input("Data file name (no extension): ")
    files = [None]*3
    files[0] = 'D:\Desktop\Academia\TRC4200\data20220429\BayId_MarkerId_2019'
    files[1] = 'D:\Desktop\Academia\TRC4200\data20220429\BayId_MarkerId_2020'
    files[2] = 'D:\Desktop\Academia\TRC4200\data20220429\BayId_MarkerId_2018'
    with open('data_filtered' + '.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        IdList[0][0] = 'BayId'
        IdList[1][0] = 'StreetMarker'
        for data in files:
            with open(data + '.csv', 'r') as inp:
                j = 0
                for row in csv.reader(inp):
                    if j == 0:
                        BayId = row.index('BayId')
                        MarkerId = row.index('StreetMarker')
                    else:
                        if IdList[1][int(row[BayId])+1] == 0:
                            IdList[1][int(row[BayId])+1] = row[MarkerId]
                    print(j)
                    j += 1
        writer.writerows(IdList)


if __name__ == '__main__':
    Main()
