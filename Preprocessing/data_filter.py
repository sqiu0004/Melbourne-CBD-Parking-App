import csv


BayId = None
ArrivalTime = None
DepartureTime = None
StreetMarker = None
VehiclePresent = None
Largest_BayId = 0


def id_list_init(path = "D:/Desktop/Academia/TRC4200/results/id_table.csv"):
    """Converts list of marker ids to list"""
    with open(path, 'r') as id_file:
        next(id_file)
        id_reader = csv.reader(id_file, delimiter=',', quotechar="'")
        markerId_list = [row[1:] for row in id_reader]
        markerId_list = markerId_list[0]

    return markerId_list


def Main():
    data = input("Data csv name (with extension): ")
    # D:\Desktop\Academia\TRC4200\data\data2017.csv
    markerId_list = id_list_init()

    with open(data, 'r') as inp, open('data_filtered.csv', 'w', newline='') as out:
        fieldnames = ['BayId', 'ArrivalTime', 'DepartureTime', 'StreetMarker']
        writer = csv.DictWriter(out, fieldnames)
        reader = csv.reader(inp)

        i = 0
        j = 0
        k = 0

        for row in reader:
            print(row)
            ArrivalTime = row.index('ArrivalTime')
            DepartureTime = row.index('DepartureTime')
            StreetMarker = row.index('StreetMarker')
            VehiclePresent = row.index('Vehicle Present')

            writer.writerow({'BayId': 'BayId',
                             'ArrivalTime': 'ArrivalTime',
                             'DepartureTime': 'DepartureTime',
                             'StreetMarker': 'StreetMarker'})

            try:
                BayId = row.index('BayId')
            except:
                BayId = -1

            break


        for row in reader:
            j += 1
            if (row[VehiclePresent].lower() != "false") and (row[VehiclePresent] != "0"):
                if BayId == -1:
                    try:
                        row.append(markerId_list.index(row[StreetMarker]))
                    except:
                        k += 1
                        continue

                i += 1
                print("i: ", i, "   j: ", j, "   k: ", k, "   Present: ", row[VehiclePresent])

                writer.writerow({'BayId': row[BayId],
                                 'ArrivalTime': row[ArrivalTime],
                                 'DepartureTime': row[DepartureTime],
                                 'StreetMarker': row[StreetMarker]})

if __name__ == '__main__':
    Main()

# 0: DeviceId
# 1: ArrivalTime
# 2: DepartureTime
# 3: StreetMarker
# 4: BayId
# 5: SignPlateID
# 6: Sign
# 7: AreaName
# 8: BayId
# 9: StreetName
# 10: BetweenStreet1ID
# 11: BetweenStreet1
# 12: BetweenStreet2ID
# 13: BetweenStreet2
# 14: SideOfStreet
# 15: SideOfStreetCode
# 16: SideName
# 17: BayId
# 18: InViolation
# 19: VehiclePresent
