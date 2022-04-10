#Parking Space Data Preprocessing
##The data
###Columns: BayId, ArrivalTime, DepartureTime, DurationMinutes
- BayId: id of parking bay
- ArrivalTime: time a vehicle arrives at the parking bay
- DepartureTime: time the vehicle departs the parking bay
- DurationMinutes: duration which the vehicle was parked
##data_filter.py
Gets raw Melbourne CBD parking data and writes the relevant information into a new csv file.
##preprocess.py
Gets filtered Melbourne CBD parking data from data_filter.py and uploads it to a MySQL database. User selects the .csv file and uploads it to a table in the database.
##reader.py
Allows users to read information about the database and rename tables. 
