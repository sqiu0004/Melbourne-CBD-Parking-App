import csv

def Main():
    data = input("Data csv name (no extension): ")

    with open(data + '.csv', 'r') as inp, open(data + '_filtered.csv', 'w', newline='') as out:
        fieldnames = ['BayId', 'ArrivalTime', 'DepartureTime', 'DurationMinutes']
        writer = csv.DictWriter(out, fieldnames)

        i = 0
        j = 0
        for row in csv.reader(inp):
            j = j + 1
            if row[-1] != "false":
                i = i + 1
                print("i: ", i, "   j: ", j)

                writer.writerow({'BayId': row[17],
                                 'ArrivalTime': row[1],
                                 'DepartureTime': row[2],
                                 'DurationMinutes': row[3]})
                # if i == 10: break

if __name__ == '__main__':
    Main()

# 0: DeviceId
# 1: ArrivalTime
# 2: DepartureTime
# 3: DurationMinutes
# 4: StreetMarker
# 5: SignPlateID
# 6: Sign
# 7: AreaName
# 8: StreetId
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
