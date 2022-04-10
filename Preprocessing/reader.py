import pymysql
import time

Endpoint = input("Host endpoint: ")
UserName = "admin"
Password = "password"
DatabaseName = "TRC4200DB"


def Main():
    SQLConnection = pymysql.connect(host=Endpoint, user=UserName, password=Password)
    SQLCursor = SQLConnection.cursor()

    while True:
        if CheckIfDatabaseExists(SQLCursor, DatabaseName):
            break
        else:
            print("Database not yet created...")
            SQLConnection.commit()
            time.sleep(1)

    SelectDatabase(SQLCursor, DatabaseName)
    ShowTables(SQLCursor)
    table = input("\nChoose table: ")

    while True:
        if CheckIfTableExists(SQLCursor, table):
            break
        else:
            print("Table not yet created...")
            SQLConnection.commit()
            time.sleep(1)

    print("\n1. Rename table \n2. Table info")
    user_command = input("What would you like to do? ")
    if user_command == "1":
        RenameTable(SQLCursor, SQLConnection, table)
        ShowTables(SQLCursor)
    elif user_command == "2":
        print("Loading table info...")
        TableInfo(SQLCursor, table)


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


def SelectDatabase(Cursor, Name):
    try:
        Cursor.execute(f"use {Name}")
        Cursor.connection.commit()
    except Exception as e:
        print(e)


def ShowTables(Cursor):
    Cursor.execute("Show tables;")
    myresult = Cursor.fetchall()

    print("\nTables: ")
    for x in myresult:
        print(x)


def TableInfo(Cursor, table):
    Cursor.execute(f"select * from {table}")
    fetch = Cursor.fetchall()
    print("Table length: ", len(fetch))

    i = 0
    for row in fetch:
        i = i + 1
        if i == 1:
            print("First row: ", row)
        elif i == 2:
            print("Second row: ", row)
            break


def RenameTable(Cursor, Connection, table):
    while True:
        print("\nRename ", table, " to: ")
        new_name = input()
        if CheckIfTableExists(Cursor, new_name):
            print("Table with name already exists! ")
        else:
            Cursor.execute("ALTER TABLE " + table + " RENAME TO " + new_name)
            Connection.commit()


if __name__ == '__main__':
    Main()