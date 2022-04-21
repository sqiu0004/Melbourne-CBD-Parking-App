import csv
import pymysql

Endpoint = input("Host endpoint: ")
UserName = "admin"
Password = "password"
DatabaseName = "TRC4200DB"


def Main():
    SQLConnection = pymysql.connect(host=Endpoint, user=UserName, password=Password)
    SQLCursor = SQLConnection.cursor()

    if not CheckIfDatabaseExists(SQLCursor, DatabaseName): # check if a database exists before trying to delete or create one with the same name
        CreateDatabase(SQLCursor, DatabaseName) # create a database before we can start creating tables
    SelectDatabase(SQLCursor, DatabaseName) # select it before trying to create a table within it

    SQLCursor.execute("show databases")
    Databases = SQLCursor.fetchall()
    print(f"Databases after creation: {Databases}")

    data = input("Enter data source name: ")

    if not CheckIfTableExists(SQLCursor, data):
        create_confirm = input("Table does not exist. Create table? (y/n): ")
        if create_confirm == "y":
            SQLCursor.execute("CREATE TABLE " + data + " (BayId varchar(32), ArrivalTime varchar(32), DepartureTime varchar(32), DurationMinutes varchar(32))")
            print("Created table: ", data)

    confirm = input("Write to table? (y/n) ")
    if confirm == "y":
        with open(data + '.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            i = 0  # counter
            batch = []
            for row in reader:
                i = i + 1
                print("i: ", i)
                batch.append([row[0],row[1],row[2],row[3]])
                if i % 1000000 == 0:
                    PopulateTableBatch(SQLCursor, SQLConnection, batch, data)
                    batch.clear()
            if len(batch) > 0:
                PopulateTableBatch(SQLCursor, SQLConnection, batch, data)

    SQLCursor.execute(f"select * from {data}")
    pe_table = SQLCursor.fetchall()
    for row in pe_table:
        print("First entry: ", row)
        break
    print("Database length", len(pe_table))


def PopulateTableBatch(Cursor, Connection, batch, data):
    Cursor.executemany(f"INSERT INTO {data} (BayId, ArrivalTime, DepartureTime, DurationMinutes) values(%s, %s, %s, %s)", batch)
    Connection.commit()


def CheckIfTableExists(Cursor, Name):
    Cursor.execute('show tables')
    Tables = Cursor.fetchall()

    for Table in Tables:
        if Table[0] == Name:
            return True

    return False


def CheckIfDatabaseExists(Cursor, Name):
    Cursor.execute('show databases')
    Databases = Cursor.fetchall()

    for Database in Databases:
        if Database[0] == Name:
            return True

    return False


def CreateDatabase(Cursor, Name):
    Cursor.execute(f"create database {Name}")
    Cursor.connection.commit()


def SelectDatabase(Cursor, Name):
    try:
        Cursor.execute(f"use {Name}")
        Cursor.connection.commit()
    except Exception as e:
        print(e)


def DeleteDatabase(Cursor, Name):
    Cursor.execute(f"drop database {Name}")
    Cursor.connection.commit()


if __name__ == '__main__':
    Main()
